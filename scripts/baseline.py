"""从固定本地模型生成一条可复现的推理记录。仓库根目录运行。"""
import argparse
import hashlib
import importlib.metadata
import json
import platform
import time
from datetime import datetime, timezone
from pathlib import Path


def file_hash(path):
    digest = hashlib.sha256()
    with path.open('rb') as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b''):
            digest.update(chunk)
    return digest.hexdigest()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--output', type=Path, required=True)
    parser.add_argument('--adapter-path', type=Path)
    args = parser.parse_args()
    if args.output.exists():
        parser.error('输出文件已存在，请为本次运行指定新路径')

    import mlx.core as mx
    from mlx_lm import load, generate
    from mlx_lm.sample_utils import make_sampler

    config = json.loads(Path('configs/model.json').read_text())
    model_path = Path(config['local_path'])
    if not (model_path / 'config.json').exists():
        parser.error('本地模型尚未下载完成')
    model, tokenizer = load(str(model_path), adapter_path=str(args.adapter_path) if args.adapter_path else None)
    messages = [{'role': 'user', 'content': '请用简体中文简短回答：无常是否意味着努力没有意义？如果没有核对经典，请勿编造佛经引文。'}]
    prompt = tokenizer.apply_chat_template(messages, tokenize=False, add_generation_prompt=True, enable_thinking=False)
    mx.random.seed(42)
    start = time.monotonic()
    answer = generate(model, tokenizer, prompt=prompt, max_tokens=256,
                      sampler=make_sampler(temp=0.7, top_p=0.8, top_k=20), verbose=False)
    elapsed = time.monotonic() - start
    record = {
        'created_at': datetime.now(timezone.utc).isoformat(),
        'model': config,
        'model_file_hashes': {str(p.relative_to(model_path)): file_hash(p)
                              for p in sorted(model_path.iterdir()) if p.is_file()},
        'adapter_path': str(args.adapter_path) if args.adapter_path else None,
        'adapter_file_hashes': {str(p.relative_to(args.adapter_path)): file_hash(p)
                                for p in sorted(args.adapter_path.rglob('*')) if p.is_file()} if args.adapter_path else {},
        'python': platform.python_version(),
        'packages': {name: importlib.metadata.version(name) for name in ['mlx', 'mlx-lm', 'transformers']},
        'device': mx.device_info(),
        'messages': messages, 'rendered_prompt': prompt,
        'chat_template': tokenizer.chat_template,
        'generation': {'seed': 42, 'temperature': 0.7, 'top_p': 0.8, 'top_k': 20, 'max_tokens': 256, 'enable_thinking': False},
        'answer': answer, 'generation_seconds': elapsed,
        'peak_memory_bytes': mx.get_peak_memory(),
        'review_status': 'pending',
        'note': '流程冒烟测试，不是独立质量评估；本题不得充作未见过的测试题。',
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    with args.output.open('x', encoding='utf-8') as stream:
        json.dump(record, stream, ensure_ascii=False, indent=2)
        stream.write('\n')
    print(answer)
    print(f'\n记录：{args.output}；生成耗时：{elapsed:.2f}s')


if __name__ == '__main__':
    main()

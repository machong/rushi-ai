"""旧的原文解经实验已停用，历史记录仍保留。"""
import argparse


def main():
    parser = argparse.ArgumentParser(description='旧实验入口已停用：经义回答须以用户认可老师的实际讲解为依据。')
    parser.add_argument('--output')
    parser.parse_args()
    parser.error('尚未补齐老师讲解及出处；停止原文驱动的 AI 解经实验。请先完成 docs/commentary_policy.md 中的资料流程。')


if __name__ == '__main__':
    main()

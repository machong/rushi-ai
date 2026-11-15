# Rushi App（如是）｜App Store 发布与 CI/CD 自动化方案

> 版本：v0.1  
> 制定日期：2026-11-12  
> 状态：2026-11-15 已完成当前仓库检查；Git 仓库已关联，尚未定位到 App 工程；Apple Developer 账号尚未开通。  
> 目标：先开发可发布的首版 iOS App，再通过 TestFlight 验证和 App Store 审核，逐步建立 CI/CD。
>
> 当前准备记录与首版建议见 [首次发布准备工作单](appstore-release-readiness.md)。原方案中“现有版本”及阶段 A 的源码检查，须在 App 工程建立后执行。

## 1. 项目目标与范围

### 目标

1. **首次上架**：将当前可用的 Rushi App 发布到 Apple App Store。
2. **持续集成（CI）**：代码提交后自动执行检查、编译和测试，及时发现问题。
3. **持续交付/发布（CD）**：合格版本自动构建、签名、上传 TestFlight；经授权后自动提交 App Store 审核。
4. **审核通过后发布**：根据 App Store Connect 配置，审核通过后自动上架，或保留人工确认发布选项。
5. **安全与可追溯**：保留构建日志、版本号、发布记录；关键发布权限和密钥受到保护。

### 不在本阶段内

- 不要求在首次上架前完成「如是」AI Agent 的长期训练目标。
- 不重构现有 App，不在未检查代码前预设其技术栈。
- 不让 AI Agent 无审核地直接修改生产配置或发布正式版本。

## 2. 推荐技术架构

**首选：GitHub + GitHub Actions + Fastlane + App Store Connect**

```text
开发者 / AI Agent 修改代码
          ↓
      GitHub 仓库
          ↓
  Pull Request（PR）
          ↓
 CI：代码检查 → 编译 → 自动测试
          ↓
     合并到 main
          ↓
 CD：构建 → 签名 → 上传 TestFlight
          ↓
     测试与验收
          ↓
  创建版本标签 v1.0.0
          ↓
  受保护的发布任务（可要求人工批准）
          ↓
  自动提交 App Store 审核
          ↓
        Apple 审核
          ↓
审核通过后：自动上架 / 人工点击发布
```

**重要边界**：自动化可以完成构建、测试、上传、提交审核和审核通过后的发布配置，**不能绕过 Apple 的审核或保证审核通过**。

**备选：Xcode Cloud**。如果后续发现 GitHub Actions 的 macOS 构建、签名维护成本较高，可评估 Xcode Cloud；正式选型时再核对当时的计费、用量及功能限制。

## 3. 首次发布需要准备的事项

### 3.1 Apple 开发者与 App Store Connect

- [ ] 开通或确认 **Apple Developer Program** 会员（通常为 US$99/年或当地等值价格，以官方结算为准）。
- [ ] 确定以**个人**还是**法人**身份发布。若以法人发布，核实公司信息及可能需要的 D-U-N-S 验证。
- [ ] 在 App Store Connect 创建 Rushi App 记录。
- [ ] 确定应用名称、主语言、Bundle ID（例如 `com.example.rushi`；**仅为占位示例**）、SKU。
- [ ] 配置 App ID、证书及 Provisioning Profile，或选择适合的自动签名方案。
- [ ] 确认最新有效的 Xcode 与 iOS SDK 上传要求；在实际构建时以 Apple 官方要求为准。

### 3.2 App 可发布性

- [ ] 明确技术栈：Swift/SwiftUI、React Native、Flutter 或其他。
- [ ] 在适配的 macOS + Xcode 环境下能够成功构建 Release 版本。
- [ ] 真机测试核心流程，排查崩溃、登录、网络、对话与错误处理。
- [ ] 整理版本号（`MARKETING_VERSION`）与 Build Number（`CURRENT_PROJECT_VERSION` 或技术栈等效配置）。
- [ ] 检查正式环境 API 地址、密钥管理、日志及错误上报，**不得将 API Secret 写入客户端代码或 Git 仓库**。

### 3.3 上架资料

- [ ] App 名称、副标题、简介、关键词、分类。
- [ ] App 图标和符合 Apple 当前尺寸要求的商店截图。
- [ ] 隐私政策 URL、支持 URL / 联系方式。
- [ ] App Privacy 数据收集与共享声明。
- [ ] 年龄分级、内容权利及其他 App Store Connect 必填问卷。
- [ ] 若审核必须登录，提供测试账号或在审核说明中说明可访问的测试方式。
- [ ] 必要时提供出口合规、加密使用和相关地区的监管申报信息。

## 4. Rushi App 特殊合规与质量要求

如是是面向公众的佛法 AI 应用，除普通 iOS 审核要求外，应重点检查：

1. **佛学内容溯源**：区分经典原文、祖师/讲者注释与 AI 归纳推论，不杜撰经文或出处；不声称 AI 已证悟或具备真实修行境界。
2. **知识与素材版权**：核实经文译本、视频字幕、讲经内容、图片、音频和训练数据的使用授权。公开视频不等于可任意训练或再发布。
3. **隐私与第三方 AI**：对对话内容、账号信息、分析数据以及第三方模型服务的处理方式作真实披露，落实必要的用户同意与安全措施。
4. **内容安全**：处理不适当输出、用户反馈、滥用和错误信息，不以恐吓、操控或制造依赖的方式交流。
5. **账号及数据删除**：如果 App 支持创建账号，应检查适用的应用内账号删除与数据处理要求。
6. **可用性**：审核时后端服务应可访问，功能说明和应用实际行为一致。

> 注：上述为上架准备检查项，不代替 Apple 最新审核指南、隐私法规或法律意见。

## 5. GitHub CI/CD 触发规则

| 触发条件 | 自动执行 | 发布权限 |
| --- | --- | --- |
| Pull Request | 依赖安装、静态检查、编译、单元测试 | 不允许正式发布 |
| 合并到 `main` | 完整 CI、生成内部测试构建、上传 TestFlight | 限制在测试分发 |
| 创建 `v*` 版本标签 | 版本校验、Release 构建、签名、商店资料核对、提交审核 | 通过受保护 Environment 授权 |
| App Store 审核通过 | 按 App Store Connect 发布模式自动上架，或人工发布 | 依所选发布模式 |
| 构建/上传/审核失败 | 保存日志，通知负责人，停止后续步骤 | 不继续发布 |

### 建议的分支与版本规范

- `main`：当前稳定的候选发布代码。
- `feature/*`：功能分支，经 Pull Request 审查后合并。
- `v1.0.0`、`v1.0.1`：正式版本标签，触发生产发布流程。
- 每次发布保留 Git commit、版本号、构建编号、变更说明、TestFlight/App Store 状态。

### 签名与密钥管理

- CI 使用 **macOS runner** 进行原生 iOS 构建。
- Fastlane 管理构建、签名、上传与 App Store Connect 操作。
- 采用 App Store Connect API Key 或 Apple 支持的安全认证方式。
- 证书、Provisioning Profile、API Key 等保存在受控的密钥存储中；绝不写入源码。
- 生产发布使用 **GitHub Environments + 审批/分支限制**；首次发布优先保留人工批准步骤。
- 对签名证书、密钥和发布权限设置轮换、撤销及最小权限策略。

## 6. 建议的仓库交付结构

根据实际技术栈调整，预期至少包含：

```text
rushi-app/
├── README.md
├── ...                        # 现有 App 代码与 Xcode 工程
├── .github/
│   └── workflows/
│       ├── ios-ci.yml         # PR：构建与测试
│       ├── testflight.yml     # main：内部测试分发
│       └── appstore.yml       # tag：正式发布
├── fastlane/
│   ├── Fastfile              # 构建、上传、发布任务
│   ├── Appfile               # 应用标识及账号配置
│   └── metadata/             # 可选：商店文案元数据
├── Gemfile                   # Fastlane 依赖版本（如适用）
└── docs/
    └── appstore-release.md  # 发布操作与回滚说明
```

> 以上是**目标结构**，不是已创建或已部署的文件。真正编写 Workflow 前须先检查当前仓库。

## 7. 推荐实施顺序

### 阶段 0｜首版产品与工程（当前阶段）

- [x] 检查当前仓库：`rushi-ai` 为 Python 模型训练项目，无 iOS App 工程。
- [x] 确认起点：Git 仓库已关联，尚未定位到 App 工程；Apple Developer 账号尚未开通。
- [ ] 确认首版功能、模型服务和数据处理方式，见首次发布准备工作单。
- [ ] 建立 App 工程，并安装与 Apple 当前上传要求相容的完整 Xcode。
- [ ] 开通 Apple Developer Program，确定发布主体。
- [ ] 完成首版实现、本地构建与真机验证，再进入阶段 A/B。

**完成标志**：存在可运行的 App 工程；发布主体和后端方案明确。

### 阶段 A｜检查现有版本（优先）

- [ ] 获取 Rushi App GitHub 仓库地址与访问权限。
- [ ] 阅读项目结构、技术栈、依赖与现有自动化配置。
- [ ] 在本地 macOS / Xcode 验证构建与基本运行。
- [ ] 给出「可立即发布 / 需要修复」差距清单。

**完成标志**：已有可重复构建的 iOS App，明确首次发布的阻塞点。

### 阶段 B｜首次 TestFlight

- [ ] 配置 Apple Developer、Bundle ID、签名及 App Store Connect。
- [ ] 编写 `ios-ci.yml`，使 PR 自动编译和测试。
- [ ] 配置 Fastlane 和 TestFlight 上传流程。
- [ ] 在 TestFlight 安装并验证当前版本。

**完成标志**：至少一次从 GitHub 自动构建并成功上传 TestFlight。

### 阶段 C｜首次 App Store 发布

- [ ] 准备商店文案、截图、隐私政策和必填信息。
- [ ] 完成 App Privacy / 合规问卷，准备审核说明。
- [ ] 创建首个正式版本并提交 Apple 审核。
- [ ] 处理审核反馈，审核通过后公开发布。

**完成标志**：Rushi App 在指定 App Store 地区可被用户下载。

### 阶段 D｜持续发布自动化

- [ ] 配置 `v*` 标签触发的受保护发布流程。
- [ ] 自动生成构建号、上传正式包及关联发布说明。
- [ ] 视 API 能力与商店配置，自动提交审核与设置上架模式。
- [ ] 加入失败通知、发布记录、必要的人工审批与紧急暂停机制。

**完成标志**：日常版本更新不再依赖逐次手工归档和上传 Xcode 构建包。

## 8. 风险与控制

| 风险 | 控制建议 |
| --- | --- |
| Apple 审核未通过 | 预先检查指南、准备审核账号与说明；保留修复后重新提交路径 |
| 签名/证书到期 | 集中管理证书和到期提醒，避免个人电脑成为唯一可发布环境 |
| AI Agent 误触发上架 | 正式发布只接受受保护标签和授权审批 |
| API Key 泄漏 | 最小权限、密钥存储、定期轮换；不进入仓库和客户端包 |
| 应用依赖后端或第三方模型 | 加入服务可用性检查；设置调用限额及失败处理 |
| 发布后出现严重缺陷 | 保留已知稳定版本；准备修复版本与服务端降级/功能开关方案。App Store 已上架包不能像网页一样即时回滚 |

## 9. 下一步需要确认的信息

1. Rushi App 的 **GitHub 仓库 URL**（以及访问方式）。
2. App 使用什么技术栈？当前是否能在 Mac 上用 Xcode 成功运行？
3. Apple Developer Program 是否已开通？以个人还是法人身份上架？
4. App 是否有账号登录、后端 API、AI 模型服务及用户聊天记录存储？
5. 第一版希望使用「审核通过自动上架」，还是「审核通过后人工确认」？

**当前建议**：先完成阶段 A 的仓库/构建检查，然后按阶段 B → C → D 逐步打通。不把长期模型训练项目与 App 首次上架绑定。

## 10. 官方参考入口

- Apple Developer Program：https://developer.apple.com/programs/
- App Store Connect：https://appstoreconnect.apple.com/
- App Review Guidelines：https://developer.apple.com/app-store/review/guidelines/
- App Store Connect API：https://developer.apple.com/documentation/appstoreconnectapi
- GitHub Actions：https://docs.github.com/en/actions
- GitHub Environments：https://docs.github.com/en/actions/how-tos/deploy/configure-and-manage-deployments/manage-environments
- Fastlane：https://docs.fastlane.tools/

---

**原则**：Rushi 的发布流程应该可靠、可审计、可恢复，而不是为了“全自动”牺牲安全。首次发布允许适度人工审核；稳定后再逐步提高自动化程度。

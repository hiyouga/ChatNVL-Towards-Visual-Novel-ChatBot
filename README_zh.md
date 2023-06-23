# ChatNVL! Chat with Characters in Visual Novels

![GitHub Repo stars](https://img.shields.io/github/stars/hiyouga/ChatNVL-Towards-Visual-Novel-ChatBot?style=social)
![GitHub Code License](https://img.shields.io/github/license/hiyouga/ChatNVL-Towards-Visual-Novel-ChatBot)
![GitHub last commit](https://img.shields.io/github/last-commit/hiyouga/ChatNVL-Towards-Visual-Novel-ChatBot)
![GitHub pull request](https://img.shields.io/badge/PRs-welcome-blue)

“如果世界上有机器人能够像人一样微笑，一样哭泣，一样悲伤。你会怎样想呢？”

<p align="right">
—— 露西 -她所期望的一切-（2016）
</p>

👋 加入我们的[QQ群](assets/qq.jpg)。

\[ [English](README.md) | 中文 \]

## 引言

在过去的几十年中，人类和机器人之间的爱情故事成为无数文学作品和视觉小说中的一个流行题材。读者们或许会幻想在不久的将来，人工智能（AI）能够具备真正的情感。最近，随着预训练语言模型的飞速发展，[ChatGPT](https://openai.com/blog/chatgpt) 及其同类产品展现出了惊人的对话能力，尤其是能给出符合人类偏好的回答。尽管如此，这些机器人的首要目标仍然是遵循人类指令，充当智能助手的角色。它们并不具备个性，因此人类很难与它们共情。虽然我们能设计包含角色描述的提示词（prompts）命令 AI 进行角色扮演，但这种方法仍存在以下几个弊端：

- AI 容易在多轮对话后忘记角色的信息。
- AI 的对话效果很大程度取决于提示词的质量。
- AI 有时会拒绝人类的交流。
- AI 无法利用用户的反馈更新自己的知识。

尽管存在上述弊端，AI 仍具有利用预训练知识来模仿任意虚拟角色的潜力。提示词的效果不尽人意主要是因为 AI 自身的知识没有被修改。与此相反，我们猜测利用合适的语料对预训练语言模型进行微调，尽可能地对齐虚拟角色的行为，将是一种更有效的方法。因此，在本项目中，我们希望利用最先进的训练技巧来微调预训练语言模型，从而生成与任意虚拟角色行为相似的 AI。由此，视觉小说中描述的梦幻场景也许能够得到实现。

## 我们将要做什么？

### 1. 数据集构建

首先，我们会利用视觉小说中的脚本来生成微调数据集，包含以下几个步骤：

- 从游戏脚本中提取多轮对话。
- 过滤掉数据中的专有信息，例如命名实体和专业术语。
- 利用 ChatGPT 将语料重建为指令数据集，从而缓解微调过程中的领域偏移问题。

数据集包含以下两种类型：

- 角色描述数据集。
  - 每条样本是一个问答对，包含角色的基本信息，例如`名字`、`年龄`和`爱好`。
- 对话数据集。
  - 每条样本包含一个情境对话，其中有该角色的回答。它既可能是单轮对话也可能是多轮对话。

目前我们正在处理以下几部视觉小说：

- 恋×シンアイ彼女（已完成）
- サノバウィッチ（已完成）
- 千恋＊万花（已完成）
- ハミダシクリエイティブ（进行中）

### 2. 语言模型微调（关键部分）

我们的工作基于在大量中文语料上经过训练的大型语言模型。受 ChatGPT 启发，我们采用的微调范式是监督微调（SFT）和强化学习（RLHF）。模型微调主要依赖于 [LLaMA-Efficient-Tuning](https://github.com/hiyouga/LLaMA-Efficient-Tuning) 和 [ChatGLM-Efficient-Tuning](https://github.com/hiyouga/ChatGLM-Efficient-Tuning) 框架，更多详细内容请移步这些项目。

### 3. 多模态特征加持

该项目生成的 AI 能够加入以下多模态组件：

- [VITS](https://github.com/jaywalnut310/vits) - 语音生成。
- [Live2D](https://www.live2d.com/) - 动态 2D 立绘。
- [Whisper](https://openai.com/research/whisper) - 自动语音识别。

## 与同类项目的比较

- [ChatGPT](https://chat.openai.com/)
- [New Bing](https://www.bing.com/search?q=Bing+AI)
- [CharacterAI](https://beta.character.ai/)

## 潜力和影响

我们认为该项目具备十分乐观的潜能和深远的影响，鉴于：

- 我们提供了一个针对指令式语言模型的详细微调流程。
- 我们探索了 AI 驱动的聊天机器人在模仿人类上的能力。
- 我们展示了一种定制符合用户个人偏好的聊天机器人的可行方案。

## 协议

本仓库的代码依照 [Apache-2.0](LICENSE) 协议开源。

## 声明

本项目基于 [LLaMA-Efficient-Tuning](https://github.com/hiyouga/LLaMA-Efficient-Tuning) 和 [ChatGLM-Efficient-Tuning](https://github.com/hiyouga/ChatGLM-Efficient-Tuning)。

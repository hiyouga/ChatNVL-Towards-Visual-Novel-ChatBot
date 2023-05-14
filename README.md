# ChatNVL! Towards Visual Novel ChatBot

![GitHub Repo stars](https://img.shields.io/github/stars/hiyouga/ChatNVL-Towards-Visual-Novel-ChatBot?style=social)
![GitHub Code License](https://img.shields.io/github/license/hiyouga/ChatNVL-Towards-Visual-Novel-ChatBot)
![GitHub last commit](https://img.shields.io/github/last-commit/hiyouga/ChatNVL-Towards-Visual-Novel-ChatBot)
![GitHub pull request](https://img.shields.io/badge/PRs-welcome-blue)

"If there was a robot that could laugh, cry and smile. Does it have a soul?"

<p align="right">
— Lucy -The Eternity She Wished For- (2016)
</p>

👋 Join our [QQ Group](assets/qq.jpg).

\[ English | [中文](README_zh.md) \]

## Introduction

In the past decades, romance between humans and androids has become a popular theme in numerous literature and visual novels. Readers may imagine that there will be artificial intelligence (AI) capable of experiencing authentic emotions in the near future. Recently, with the rapid development of pre-trained language models (PLMs), [ChatGPT](https://openai.com/blog/chatgpt) and its analogues demonstrate stunning performance in communication with humans and especially in alignment with human preferences. However, the primary objective of these robots is to follow the human instructions so as to serve as an intelligent assistant. These robots lack characteristics and hence humans can hardly empathize with them. Although it is possible to instruct AI to perform a role-play by designing prompts containing the description of a virtual character, there are several drawbacks of this approach:

- AI tends to forget information after several turns of chat.
- AI cannot achieve satisfactory performance with ineffective prompts.
- AI sometimes refuses to follow some instruction given by humans.
- AI cannot update its knowledge according to user's feedbacks.

Despite the aforementioned limitations, AI has the potential of leveraging pretrained knowledge to imitate any virtual character. The effectiveness of prompts is questionable since the knowledge contained in AI remains unaffected. On the contrary, we conjecture that fine-tuning the PLMs under the objective of aligning their behaviors with virtual characters using the adequate corpus can achieve satisfactory results. Therefore, in this project, we aim to fine-tune the PLMs with state-of-the-art training schemes to generate AIs that behaves like arbitrary virtual characters. This will enable the realization of the dream presented in the visual novels.

## What Shall We Do?

### 1. Dataset Construction

Firstly, we will utilize the script from the visual novels to generate datasets for fine-tuning with the following steps:

- Extract the multi-turn conversation from the game script.
- Filter out the specific information in the data, including named entities and terms.
- Reconstruct the corpus to form instruction-following datasets using ChatGPT to mitigate the domain-shift problem in the fine-tuning phase.

The dataset includes two types:

- Character description dataset.
  - Each instance contains a question-answer pair about the basic information of the character, such as `name`, `age` and `hobbies`.
- Conversation dataset.
  - Each instance contains a situational dialogue along with the response of the character. It can contain either single-turn or multi-turn dialogues.

Now we are handling the following visual novels:

- 恋×シンアイ彼女 (done)
- サノバウィッチ (done)
- ハミダシクリエイティブ (in progress)

### 2. Language Model Fine-tuning (Core)

We are based on the [ChatGLM-6B](https://github.com/THUDM/ChatGLM-6B) model since its remarkable performance in Chinese NLP tasks. Inspired by ChatGPT, the paradigm of fine-tuning we adopted is supervised fine-tuning (SFT) and reinforcement learning with human feedback (RLHF). Our fine-tuning largely depends on the [ChatGLM-Efficient-Tuning](https://github.com/hiyouga/ChatGLM-Efficient-Tuning) framework. Please refer to this repo for more details.

### 3. Equipping with Multimodal Features

The generated AI can equip with the following multimodal features:

- [VITS](https://github.com/jaywalnut310/vits) - Text to speech.
- [Live2D](https://www.live2d.com/) - Animated 2D illustration.
- [Whisper](https://openai.com/research/whisper) - Automatic speech recognition.

## Compared with Existing Projects

- [ChatGPT](https://chat.openai.com/)
- [New Bing](https://www.bing.com/search?q=Bing+AI)
- [CharacterAI](https://beta.character.ai/)

## Potential and Impacts

We suppose this project may have promising potential and broad impacts because the following advantages:

- We provide an elaborated scheme to fine-tune the language model trained on instruction-following datasets.
- We explore the abilities of AI-powered chat bots to imitate the emotions of human beings.
- We demonstrate a possible way to custom user own chat bots that align with user's preference.

## License

This repository is licensed under the [Apache-2.0 License](LICENSE).

## Acknowledgement

This repo is based on [ChatGLM-6B](https://github.com/THUDM/ChatGLM-6B) and [ChatGLM-Efficient-Tuning](https://github.com/hiyouga/ChatGLM-Efficient-Tuning). Thanks for their wonderful works.

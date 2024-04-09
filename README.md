<!-- markdownlint-disable MD031 MD033 MD036 MD041 -->

<div align="center">

<a href="https://v2.nonebot.dev/store">
  <img src="https://raw.githubusercontent.com/A-kirami/nonebot-plugin-template/resources/nbp_logo.png" width="180" height="180" alt="NoneBotPluginLogo">
</a>

<p>
  <img src="https://raw.githubusercontent.com/lgc-NB2Dev/readme/main/template/plugin.svg" alt="NoneBotPluginText">
</p>

# NoneBot-Plugin-PingTi

_✨ 让 AI 帮你寻找更低价的购物搜索词 ✨_

<img src="https://img.shields.io/badge/python-3.9+-blue.svg" alt="python">
<a href="https://pdm.fming.dev">
  <img src="https://img.shields.io/badge/pdm-managed-blueviolet" alt="pdm-managed">
</a>
<a href="https://wakatime.com/badge/user/b61b0f9a-f40b-4c82-bc51-0a75c67bfccf/project/018cef6a-03d4-4902-8b19-272f441456ef">
  <img src="https://wakatime.com/badge/user/b61b0f9a-f40b-4c82-bc51-0a75c67bfccf/project/018cef6a-03d4-4902-8b19-272f441456ef.svg" alt="wakatime">
</a>

<br />

<a href="https://pydantic.dev">
  <img src="https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/lgc-NB2Dev/readme/main/template/pyd-v1-or-v2.json" alt="Pydantic Version 1 Or 2" >
</a>
<a href="./LICENSE">
  <img src="https://img.shields.io/github/license/lgc-NB2Dev/nonebot-plugin-pingti.svg" alt="license">
</a>
<a href="https://pypi.python.org/pypi/nonebot-plugin-pingti">
  <img src="https://img.shields.io/pypi/v/nonebot-plugin-pingti.svg" alt="pypi">
</a>
<a href="https://pypi.python.org/pypi/nonebot-plugin-pingti">
  <img src="https://img.shields.io/pypi/dm/nonebot-plugin-pingti" alt="pypi download">
</a>

</div>

## 📖 简介

节选自[原网站](https://www.pingti.xyz/)：

> 同一件商品，不同的搜索词，价格可能会天差地别。  
> 这个工具旨在帮助你找到最便宜的搜索词：  
> 输入你想搜索的商品名，AI 会给出低价的替代品，结果可能不准，开心就好 :)  
> 经济寒冬，商品可以平替，但你的生活无法被平替。

## 💿 安装

以下提到的方法 任选**其一** 即可

<details open>
<summary>[推荐] 使用 nb-cli 安装</summary>
在 nonebot2 项目的根目录下打开命令行, 输入以下指令即可安装

```bash
nb plugin install nonebot-plugin-pingti
```

</details>

<details>
<summary>使用包管理器安装</summary>
在 nonebot2 项目的插件目录下, 打开命令行, 根据你使用的包管理器, 输入相应的安装命令

<details>
<summary>pip</summary>

```bash
pip install nonebot-plugin-pingti
```

</details>
<details>
<summary>pdm</summary>

```bash
pdm add nonebot-plugin-pingti
```

</details>
<details>
<summary>poetry</summary>

```bash
poetry add nonebot-plugin-pingti
```

</details>
<details>
<summary>conda</summary>

```bash
conda install nonebot-plugin-pingti
```

</details>

打开 nonebot2 项目根目录下的 `pyproject.toml` 文件, 在 `[tool.nonebot]` 部分的 `plugins` 项里追加写入

```toml
[tool.nonebot]
plugins = [
    # ...
    "nonebot_plugin_pingti"
]
```

</details>

## ⚙️ 配置

在 NoneBot2 项目的`.env`文件中添加下表中的必填配置

|          配置项          | 必填 | 默认值 |                说明                |
| :----------------------: | :--: | :----: | :--------------------------------: |
|      `PINGTI_PROXY`      |  否  |   无   |         请求使用的代理地址         |
| `PINGTI_REQUEST_TIMEOUT` |  否  |  `5`   |       请求超时时间，单位为秒       |
|    `PINGTI_SEND_TIP`     |  否  | `True` | 缓存中不存在回答时是否发送提示消息 |
|   `PINGTI_RECALL_TIP`    |  否  | `True` |     发送提示消息后是否自动撤回     |

## 🎉 使用

指令：`平替`

## 📞 联系

QQ：3076823485  
Telegram：[@lgc2333](https://t.me/lgc2333)  
吹水群：[1105946125](https://jq.qq.com/?_wv=1027&k=Z3n1MpEp)  
邮箱：<lgc2333@126.com>

## 💡 鸣谢

### [pingti.xyz](https://www.pingti.xyz/)

- 服务提供

### [ilharp/koishi-plugin-pingti](https://github.com/ilharp/koishi-plugin-pingti)

- ~~抄袭~~ 借鉴

## 💰 赞助

**[赞助我](https://blog.lgc2333.top/donate)**

感谢大家的赞助！你们的赞助将是我继续创作的动力！

## 📝 更新日志

### 0.1.4

- 修复 [#2](https://github.com/lgc-NB2Dev/nonebot-plugin-pingti/issues/2)
- 兼容 Pydantic V2

### 0.1.3

- 修复无法使用的问题

### 0.1.2

- 实现 [#1](https://github.com/lgc-NB2Dev/nonebot-plugin-pingti/issues/1)：
  - 重命名配置项 `PROXY` -> `PINGTI_PROXY`
  - 添加配置项 `PINGTI_SEND_TIP`
  - 添加配置项 `PINGTI_RECALL_TIP`

### 0.1.1

- 优化部分逻辑

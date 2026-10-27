---
name: run-opencode-task
description: "Use when: 用户要求用 opencode 执行特定任务，或提到 用 opencode 跑/opencode run。"
---

# run-opencode-task

用户要求用 opencode 执行特定任务时，把 opencode 当作子智能体：理解用户意图，组织成一份自包含的任务描述，通过 `opencode run "<任务描述>"` 派发给它执行，并等待其返回结果。

## Use When

用户要求用 opencode 去做某个任务，例如「用 opencode 执行 xxx」「让 opencode 跑一下这个任务」。仅提到 opencode 而不要求执行任务时，不要触发。

## Steps

1. 理解用户意图，把任务组织成一份自包含的任务描述：opencode 没有当前会话的上下文，任务描述必须自带目标、范围、约束、涉及的文件/目录、验收标准，让它无需追问即可执行。假定 opencode 已在 PATH 中，直接在当前智能体的工作目录下派发（opencode 的工作目录必须与当前智能体的工作目录一致）：

   ```bash
   opencode run "<组织好的任务描述>"
   ```

   即调用时的 shell 当前目录就是本会话工作目录，不要 `cd` 到别处。

2. 等待命令返回。任务可能耗时较长，用 `run_in_background` 启动，然后通过 `task_output` 等待结束并读取输出；执行结束后核对退出码。

## Rules

- 派发前先理解用户意图再组织任务描述：不是逐字转发用户原话，而是把 opencode 当子智能体，补齐它缺失的上下文（目标、范围、约束、文件位置、验收标准）。
- 不使用 `-i` / 交互模式；`run` 是非交互执行。
- 调用时不得切换工作目录：opencode 必须在当前智能体的工作目录下执行，`cd` 到其他目录会改变任务上下文。
- 假定 opencode 已在 PATH 中，直接调用，不做安装路径探测。
- 命令失败时把退出码和错误输出如实反馈给用户，不自行重试。

## Notes

- opencode 的任务在其自身工作区/会话中执行，与当前会话相互独立，结果以命令输出为准。
- 长时间无输出属正常现象，继续等待，不要中断。

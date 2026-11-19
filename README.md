# Guided Lab Report · 引导式实验报告

[中文](#中文) · [English](#english)

## 中文

**Guided Lab Report** 是一个面向大学理工科课程实验的跨平台 Agent Skill，侧重化工和生物实验。它从实验目标出发，帮助你确认要算什么、画什么，并把实验数据整理成可追溯的结果、图表和报告。

### 如何工作

1. 从实验指导书、数据和可选的评分标准中提取目标。先列出计算、比较和作图清单，等你确认。
2. 保留原始读数，将修正和计算分开。验证公式、单位、拟合有效性和图表引用；记录需要补证据的地方。
3. 先比较结果与适用的理论值或参考值，再针对偏差询问你当时做了什么、观察到了什么。Agent 根据实验事实检验解释，再形成 Discussion。
4. 按需求提供引导、协作修改或起草。有合适工具时可生成带公式和原生图表的 Excel，以及带可编辑公式的 Word。报告中的计算值最多显示四位小数并去掉尾零，例如 `2.5`；计算过程保留完整精度。

### 开始使用

- **Codex**：将仓库内完整的 `guided-lab-report/` 文件夹放入个人或项目的 `.agents/skills/`。课程实验报告任务可按描述匹配，也可以用 `$guided-lab-report` 直接调用。
- **Claude Code**：将同一文件夹放入个人或项目的 `.claude/skills/`。可按任务自动匹配，也可以用 `/guided-lab-report` 调用。
- **普通聊天**：粘贴或附上 [SKILL.md](guided-lab-report/SKILL.md)。缺少文件工具时仍可使用分析清单、可复制的 Excel 公式和讨论引导。

使用时提供实验目标、你自己的数据及已有报告。指导书和评分标准有的话也可以一并提供。报告默认英文，也可指定中文。查看[跨平台使用说明](guided-lab-report/references/portability.md)和[标线脚本的输入格式](guided-lab-report/references/calibration-example.md)。

仓库包含 skill 说明、空白 Word/Markdown 模板和可选 Python 脚本。实验数据由使用者自行提供。

## English

**Guided Lab Report** is a portable agent skill for university science and engineering laboratory reports, with an emphasis on chemical engineering and biology. It starts with your lab objectives and helps turn experimental data into traceable calculations, figures, and report sections.

### How it works

1. Identify the objectives from the lab instructions, data, and optional rubric. Present a checklist of calculations, comparisons, and plots for your confirmation.
2. Preserve the original readings and record corrections separately. Verify formulas, units, fit validity, and chart references. Identify gaps in the evidence.
3. Compare the result with a suitable theoretical or reference value. Ask targeted questions about what you did and observed, then assess the possible explanations and write the discussion from the evidence.
4. Choose guided, collaborative, or drafting help. With compatible tools, the skill can produce Excel formulas and native charts, as well as Word reports with editable equations. Displayed calculations use up to four decimal places with trailing zeros removed, for example `2.5`. Calculations retain full precision.

### Getting started

- **Codex**: Copy the repository's complete `guided-lab-report/` folder into the user or project `.agents/skills/` directory. Matching lab-report tasks can select it automatically. Use `$guided-lab-report` to select it explicitly.
- **Claude Code**: Place the same folder in the user or project `.claude/skills/` directory. Use a matching prompt for automatic selection, or call `/guided-lab-report` explicitly.
- **Regular AI chat**: Paste or attach [SKILL.md](guided-lab-report/SKILL.md). Without file tools, the skill can still provide an analysis plan, paste-ready spreadsheet formulas, and discussion guidance.

Bring your lab objectives, your own data, and any existing draft. Add the lab manual and rubric if available. Reports default to English; you can request Chinese. See the [portability guide](guided-lab-report/references/portability.md) and the [optional calibration script input contract](guided-lab-report/references/calibration-example.md).

This repository contains skill instructions, blank Word and Markdown templates, and optional Python scripts. Supply your own experimental data.

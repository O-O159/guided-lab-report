# Discussion from comparison and experimental evidence

The assistant owns the analysis. It identifies the relevant comparison, quantifies a discrepancy, asks for missing experimental facts, then evaluates explanations and writes Discussion. The student supplies firsthand observations and records. Their answer need not explain a mechanism or take a position on causality.

## 1. Establish the comparison

Find the expected result in the supplied manual, a justified theoretical calculation with known inputs, a verified publication, or an independent control or certified reference. Use the applicable source and cite it. Keep temperature, composition, analytical basis, units, and method comparable. For a scalar, report the signed difference `measured − reference` in the original units, and the relative deviation with the reference denominator when meaningful. A zero reference has no defined percentage deviation. For an expected trend rather than a scalar, identify where the series diverges and quantify that difference where possible.

Compare the discrepancy with known uncertainty on either side, experimental scale, and the objective before deciding how much to investigate. A fit statistic such as R² cannot establish agreement with theory. If no compatible comparator exists, state that limitation and use any relevant internal controls, balance closure, residuals, or repeated-run consistency. Label those checks accordingly. A coherent result needs no forced search for a bad run.

Verify the model's suitability and the measurement range before computing a reference deviation. If either check fails or is pending, identify the issue and ask for the evidence or repeat measurement needed to resolve it.

## 2. Ask specific, non-leading questions

Lead with the measured value, expectation, difference, and affected condition or run. Then ask one to three factual questions tied to possible mechanisms. Reuse facts already supplied. Wait only for answers needed to make claims that depend on missing observations.

- “The sample estimate is below the reference by [difference, in the matching unit]. Was the sample diluted again before reading? Did it use the same blank as the standards?”
- “At the reported flow rate, the observed heat duty is lower than the balance estimate. Were both outlet readings recorded after the temperatures stabilized?”
- “The reading's residual in Run 4 was … [unit]. Did the display stabilize, and was anything unusual recorded at that time?” State that a residual is a model diagnostic.

Questions should let the student answer from memory or records. If the student reports no unusual event, assess the confirmed instrument specifications and method limitations directly. Record unobserved events as unknown.

### 中文追问题库

选与具体偏差有关的一到三个问题。先报数值、方向和工况，再给出问题。例如：“这个样品的测定值比参考值低［幅度和单位］。取样后是否还稀释过？如果有，取了多少、定容到多少？”

| 核对点 | 可问的事实 |
| --- | --- |
| 操作与计时 | “开始计时和开始取样分别对应哪个操作？这组有等待、中断或重测记录吗？” |
| 仪器与读数 | “这个读数记录前稳定了吗？校准和零点检查是什么时候做的？记录上有没有漂移、气泡或量程切换？” |
| 样品与试剂 | “标准样和未知样用的是同一空白吗？试剂是哪天配的？样品取用、稀释和定容体积分别是多少？” |
| 工况与稳态 | “开始采集时的温度、流量或转速实际是多少？稳态是根据哪段记录判断的？” |
| 数据选择 | “这个点来自哪一次原始读数？表中的括号、空白或重复 Run ID 表示什么？有没有记录说明为什么重测？” |

如果学生回答“可能没稳”，接着核对可观察的信息，例如波动范围、持续时间或当时有没有记录。记录能支持到哪里，因果表述就写到哪里。引导档可以给写作框架：“在 ___ 工况，结果为 ___，相较 ___ 偏 ___。根据 ___ 记录，该因素预计使 ___；尚无法判定 ___。”框架中的机制由助手核对后再填写。

## 3. Classify and estimate

Maintain a compact working record for each proposed explanation:

| Candidate explanation | Source or supporting observation | Error category | Mechanism | Predicted direction | Plausible magnitude | Consistency | Evidence status |
| --- | --- | --- | --- | --- | --- | --- | --- |

- Systematic effects bias a result in a repeatable direction under defined conditions. Random effects vary among repeats. Gross errors are identifiable mistakes requiring evidence; a large residual alone does not establish one.
- State whether the factor was observed, documented as an instrument specification, or only hypothesized. Do not present all three as equally established.
- Estimate magnitude from recorded excursions, precision specifications with a stated distribution, or an agreed sensitivity calculation. Do not invent a temperature drift, tolerance, or percentage contribution. If no bound exists, mark the magnitude unquantified.
- Distinguish bias from uncertainty. A ± uncertainty is not a correction, and an absolute deviation is not automatically an uncertainty estimate.

## 4. Test consistency

Trace `factor → measured input → calculated quantity → reported parameter`. Check the algebra and recompute within an agreed plausible range when feasible. Add a new sensitivity calculation to the agreed plan before executing it.

For fitted parameters, the direction of a pointwise change may not be the direction of the final parameter. With Arrhenius analysis, check which temperature point changed, whether actual or nominal temperatures were used, how both coordinates change, and how the fitted slope changes. Refit affected data when justified. “Temperature was low” alone cannot establish whether fitted activation energy rises or falls. Slow cooling does not by itself establish that the actual temperature was below the setpoint.

When predicted and observed directions conflict, explain the conflict and rule out that factor as a standalone explanation. Direction and magnitude agreement support plausibility. Establishing the actual cause requires confirming evidence. Several unmeasured effects cannot be assigned numerical shares of the total error.

Distinguish a verified correction from a hypothetical sensitivity check. Apply a confirmed correction in the workbook and use the updated evaluated result for the reference comparison. Preserve the old and new values as separate labelled quantities if discussing the size of the correction.

## 5. Form prose and improvements

Write the requested Discussion from the supported analysis. Cite the actual number or figure, state the direction and size of the discrepancy, explain the supported mechanism or the remaining uncertainty, and connect any improvement to the relevant mechanism or measurement gap.

Reject generic sentences such as “human error caused the difference.” If magnitude cannot be estimated, state the numerical discrepancy and the bound of the explanation honestly rather than inventing an estimate. Theoretical context may support a hypothesis, but cannot supply missing experimental events.

Keep unanswered questions and coaching notes outside the submission document. While awaiting missing facts, write the comparison and supported limitations. If the facts remain unavailable, complete the defensible Discussion by saying which cause cannot be established and why.

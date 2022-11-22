# EE463 Homework 2 Question 2

a) 5 of the most important parameters of MOSFET is listed below:
    - Drain to source breakdown voltage, V<sub>dss,max<\sub> : is the maximum voltage MOSFET can handle between the drain and source terminals.
    - Continious Drain current, I<sub>D<\sub> : is the maximum continuous current MOSFET can work with. During ON-state of the MOSFET, this amount of current can flow through the drain-source terminals.
    - Drain to source ON-resistance, R<sub>ds,on<\sub> : is the resistance between the drain and source terminals during the ON-state (conduction) mode. Conduction losses are dissipated as heat.
    - Gate charge, Q<sub>g<\sub> : is the required amount of charge to make transition between ON and OFF states.
    - Reverse-recovery time, t<sub>rr<\sub> : is the time elapsed during the body diode goes from conduction(ON) to blocking(OFF) state. This body diode is used as a freewheeling diode for the return path of the current. This parameter is important when dealing with high frequency switching operations. It limits the proper working frequency of the device.

b) Losses on the MOSFET can be divided into two:
    - Conduction losses: are the power losses occuring during the ON-state of the MOSFET which are dissipated as heat to the environment. These losses are affected by R<sub>ds,on<\sub>.
    -Switching losses: are the losses during ON-OFF transitions of the MOSFET. Since the working frequency of MOSFETs is high, these losses are important for consideration. Switching losses are affected by gate charge Q<sub>g<\sub> and reverse recovery time t<sub>rr<\sub>

c) Selecting and tabulating MOSFETs for 5A, 20A, 100A current ratings:

|      | No: | Model          | V_dss,max (V) | I_d (A) | R_ds,on (Ω) | Q_g (nC) | t_rr (ns) | Technology |
|------|-----|----------------|---------------|---------|-------------|----------|-----------|------------|
| 5A   | 1   | IRF510         | 100           | 5.6     | 0.54        | 8.3      | 100       | Si         |
|      | 2   | IXFH9N80       | 800           | 6.2     | 0.9         | 85       | 250       | Si         |
|      | 3   | IRFIB6N60A     | 600           | 5.5     | 0.75        | 49       | 530       | Si         |
|      | 4   | C2M10001705    | 1700          | 5.6     | 1.4         | 13       | 15        | SiC        |
|------|-----|----------------|---------------|---------|-------------|----------|-----------|------------|
| 20A  | 5   | IRFP360        | 400           | 23      | 0.2         | 210      | 420       | Si         |
|      | 6   | IRF640         | 200           | 18      | 0.18        | 55       | 240       | Si         |
|      | 7   | IXFH26N50P3    | 500           | 26      | 0.25        | 42       | 250       | Si         |
|      | 8   | C3M0120100K    | 1000          | 22      | 0.12        | 21.5     | 17        | SiC        |
|------|-----|----------------|---------------|---------|-------------|----------|-----------|------------|
| 100A | 9   | IRFP2907ZPbF   | 75            | 90      | 0.0045      | 180      | 41        | Si         |
|      | 10  | IRF3205        | 55            | 110     | 0.008       | 146      | 69        | Si         |
|      | 11  | IRF200P223     | 200           | 100     | 0.0115      | 68       | 105       | Si         |
|      | 12  | NTBG025N065SC1 | 650           | 106     | 0.0285      | 164      | 25        | SiC        |

Comparing the parameters of the MOSFETs, we see that there is always a trade-off between the parameters. For example as we increase the voltage level for a specific current rating, we see an increase in R<sub>ds,on<\sub> which will result in inefficiencies. Also we see the effect of new technologies like SiC on the parameters. Better operating conditions are achieved with the new emerging technologies.

d) Also selecting and tabulating MOSFETs for 10V, 100V, 500V voltage ratings:

|      | No: | Model         | V_dss,max (V) | I_d (A) | R_ds,on (Ω) | Q_g (nC) | t_rr (ns) | Technology |
|------|-----|---------------|---------------|---------|-------------|----------|-----------|------------|
| 10V  | 1   | CSD13202Q2    | 12            | 14.4    | 0.0091      | 5.1      | 28        | Si         |
|      | 2   | DMN1054UCB4-7 | 8             | 4       | 0.035       | 9.6      | 14        | Si         |
|      | 3   | SI7104DN      | 12            | 35      | 0.0037      | 23       | 80        | Si         |
|      | 4   | DMN1004UFV    | 12            | 70      | 0.0038      | 26       | 24.3      | Sİ         |
|------|-----|---------------|---------------|---------|-------------|----------|-----------|------------|
| 100V | 5   | IRF1310PbF    | 100           | 42      | 0.036       | 110      | 180       | Si         |
|      | 6   | IRL540NS/LPbF | 100           | 36      | 0.044       | 74       | 190       | Si         |
|      | 7   | FDS86141      | 100           | 7       | 0.023       | 11.8     | 69        | Si         |
|      | 8   | GS61008P-TR   | 100           | 90      | 0.0095      | 8        |           | GaN        |
|------|-----|---------------|---------------|---------|-------------|----------|-----------|------------|
| 500V | 9   | IRF840        | 500           | 8       | 0.85        | 63       | 460       | Si         |
|      | 10  | IXFP16N50P    | 500           | 16      | 0.4         | 36       | 200       | Si         |
|      | 11  | PJZ22NA50A    | 500           | 20.5    | 0.26        | 74       | 424       | Si         |
|      | 12  | IRF820        | 500           | 2.5     | 3           | 24       | 520       | Si         |

Looking at the results of the voltage ratings table, we see the trade-off between the parameters again. As we increase the voltage rating we see increases in reverse recovery time t<sub>rr<\sub> of the device. This will affect the available frequency region for proper operation. Again new emerging technologies like GaN, provides us better operating conditions, which of course with higher costs that are not seen in these tables.

e) As wwe discussed above, there are trade-offs between MOSFET parameters. If we want to improve one or two parameters; either other parameters get worse, or higher costs and new technologies are needed. For example looking at the table for current ratings in part-c, let's consider the models with numbers 8 and 11. These models have approximately same rated power, however model-8 has higher voltage rating and higher reverse-recovery time, compared to the model-11. For higher frequency applications, model-11 has better performance with lower breakdown voltage. Another example can be given from the table with voltage ratings in part-d. Considering the models 5 and 8, we can see the effect of an emerging technology like GaN. Model 8 has better performances regarding the given parameters, it has better continuous current, lowver gate charge and reverse recovery time than those of model-5. However model-8 has higher cost compared to the model-5 and the availability of the model-8 might be harder than the model-5.

Also we can see the effect of voltage rating between the model parameters. Looking at the models 3 and 6 from part-d with same current and different voltage ratings, model-3 has lower resistance, lower gate charge and lower reverse recovery time compared to the model-6 which has higher voltage rating. Same comparison can be observed between the models 7 and 9.

Looking at the effect of increase in current rating, we can compare the models 6 and 11 from the table of part-c. Models have same voltage rating and different current ratings. Model-6 with lower current rating has higher on-resistance and higher reverse recovery time. 

As engineers we should consider the budget, timeline and deliverables of the project we are working on, and arrange our designs, planning and supplies accordingly. If we select an overdesign for our work, this may result in problems with efficiency, supply, and budget. Let's say we need a MOSFET with 100 V and 7-8 A ratings. Looking at the table from part-d, if we select model 9 for better voltage rating instead of model-7, this will result in lower efficiency due to higher on-resistance and lower frequency availibility due to reverse recovery time (assuming the body diodes will be used for freewheeling).
linear layer according to [46]. The depth-wise convolution is used to extract local information with negligible extra computational cost. The motivation for inserting shortcut is similar to that of classic residual networks, which can promote the propagation ability of gradient across layers.We show that such shortcut helps the network achieve better results in our experiments.



With the aforementioned three components, the CMT block can be formulated as:

$$\begin{aligned}{\mathbf{Y}_{i}}&{{}=\operatorname{L P U}(\mathbf{X}_{i-1}),}\\ {\mathbf{Z}_{i}}&{{}=\operatorname{L M H S A}(\operatorname{L N}(\mathbf{Y}_{i}))+\mathbf{Y}_{i},}\\ {\mathbf{X}_{i}}&{{}=\operatorname{I R F F N}(\operatorname{L N}(\mathbf{Z}_{i}))+\mathbf{Z}_{i}.}\\ \end{aligned}$$

where $\mathbf{Y}_{i}$ and $\mathbf{Z}_{i}$ denote the output features of LPU and LMHSA module for the i-th block, respectively. LN denotes the layer normalization [1]. We stack several CMT blocks in each stage for feature transformation and aggregation.

#### 3.3. Complexity Analysis 

We analyze the computational cost between standard ViT [1O] and our CMT in this section. A standard transformer block consists of a MHSA module and a FFN. Given an input feature of size $n\times d,$ , the computational complexity (FLOPs) can be calculated as:

$$\begin{aligned}{\mathcal{O}(\operatorname{M H S A})}&{{}=2n d(d_{k}+d_{v})+n^{2}(d_{k}+d_{v}),}\\ {\mathcal{O}(\operatorname{F F N})}&{{}=2n d^{2}r,}\\ \end{aligned}$$

where r is the expansion ratio of FFN,$d_{k}$ and $d_{v}$ are dimensions of key and value, respectively. More specifically, ViT sets $d=d_{k}=d_{v}$ ,and $r=4$ :, the cost can be simplified as:

$$\begin{aligned}\mathcal{O}(Transformer block)&=\mathcal{O}(MHSA)+\mathcal{O}(FFN)\\&=12nd^2+2n^2d\end{aligned}$$

Under above setting, the FLOPs of CMT block is as follows:

$$\begin{aligned}\mathcal{O}(LPU)&=9nd,\\\mathcal{O}(LMHSA)&=2nd^{2}(1+1/k^{2})+2n^{2}d/k^{2},\\\mathcal{O}(IRFFN)&=8nd^{2}+36nd,\end{aligned}$$

$$\begin{aligned}\mathcal{O}(CMT block)&=\mathcal{O}(LPU)+\mathcal{O}(LMHSA)+\mathcal{O}(IRFFN)\\&=10nd^{2}(1+0.2/k^{2})+2n^{2}d/k^{2}+45nd\end{aligned}(16)$$

where $k\geq1$ is the reduction ratio in LMHSA. Compared to standard transformer block, the CMT block is more friendly to computational cost, and is easier to process the feature map under higher resolution (larger n).



#### 3.4. Scaling Strategy 

Inspired by [53], we propose a new compound scaling strategy suitable for transformer-based networks, which uses a compound coefficient φ to uniformly scale the number of layers (depth), dimensions, and input resolution in a principled way:

$$\begin{aligned}&depth:\alpha^{\phi},\quad dimension:\beta^{\phi},\quad resolution:\gamma^{\phi},\\ &\quad s.t.\quad\alpha\cdot\beta^{1.5}\cdot\gamma^{2}\approx2.5,\quad\alpha\geq1,\beta\geq1,\gamma\geq1\\ \end{aligned}$$

where α,$\beta,$ and γ are constants determined by grid search to decide how to assign resources to network depth, dimension and input resolution, respectively. Intuitively, φ is the coefficient that controls how many more $(\phi\geq1)$ or less $(\phi\leq-1)$ )resources are available for model scaling. Notably,the $\mathrm{F L O P s}$ of the proposed CMT block is approximately proportional1 to $\alpha,\beta^{1.5}$ , and $\gamma^{2}$ (cid:1)according to E.q. 16. And we constraint $\alpha\cdot\beta^{1.5}\cdot\gamma^{2}\approx2.5$ so that for a given new $\phi$ , the total FLOPS will approximately increase by 2.5φ. This will strike a balance between the increase of computational cost and performance gain. In our experiments, we empirically set $\alpha=1.2,\beta=1.3,\mathrm{and}\gamma=1.15$ 



We build our model CMT-S to have similar model size and computation complexity with DeiT-S (ViT-S) and EfficientNet-B4. We also introduce CMT-Ti, CMT-XS and CMT-B according to the proposed scaling strategy. The input resolutions are $1\widetilde{6}0^{2},19\widetilde{2^{2}},\widetilde{2}24^{2}$ ,and $256^{2}$ for all four models, respectively. The detailed architecture hyper-parameters are shown in Table 1.



### 4. Experiments 

In this section, we investigate the effectiveness of CMT architecture by conducting experiments on several tasks including image classification, object detection, and instance segmentation. We first compare the proposed CMT with previous state-of-the-art models on above tasks, and then ablate the important elements of CMT.



#### 4.1. ImageNet Classifi cation 

Experimental Settings. ImageNet [8] is a image classification benchmark which contains 1.28M training images and 50K validation images of 1000 classes. For fair comparisons with recent works, we adopt the same training and augmentation strategy as that in DeiT [57],$i.e.$ , models are trained for 300 epochs (800 for CMT-Ti that requires more epochs to converge) using the AdamW [37] optimizer. All models are trained on 8 NVIDIA Tesla V100 GPUs.

Results of CMT. Table 2 shows the performances of the proposed CMTs that are scaled from the CMT-S according to E.q. 17. Our models achieve better accuracy with fewer parameters and FLOPs compared to other convolution-based and transformer-based counterparts. In particular, our CMTS achieves 83.5% top-1 accuracy with 4.0B FLOPs, which is 
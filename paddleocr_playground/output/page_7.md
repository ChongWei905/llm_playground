<div style="text-align: center;">Table6. Object detectionresultson COCO val2017.All models use RetinaNet[34] as basic frameworkand are trained in $ \text{"}1x\text{"}$ schedule.FLOPs are calculated on $1280\times800$ input.  means the results are from [5]. </div>



<div style="text-align: center;"><html><body><table border="1"><tbody><tr><td>Backbone</td><td># Params</td><td># FLOPs</td><td>mAP = </td><td>$\mathrm{AP_{50}}$</td><td>= $\mathrm{AP_{75}}$</td><td>$\mathrm{A P_{S}}$</td><td>$\mathrm{AP_{M}}$</td><td>$\mathrm{AP_{L}}$</td></tr><tr><td>ConT-M [66]</td><td>27.0M</td><td>217B</td><td>37.9</td><td>58.1</td><td>40.2</td><td>23.0</td><td>40.6</td><td>50.4</td></tr><tr><td>ResNet-101 [16]</td><td>56.7M</td><td>315B</td><td>38.5</td><td>57.6</td><td>41.0</td><td>21.7</td><td>42.8</td><td>50.4</td></tr><tr><td>RelationNet++ [4]</td><td>39.0M</td><td>266B</td><td>39.4</td><td>58.2</td><td>42.5</td><td>=</td><td>=</td><td>-</td></tr><tr><td>ResNeXt-101-32x4d [64]</td><td>56.4M</td><td>319B</td><td>39.9</td><td>59.6</td><td>42.7</td><td>22.3</td><td>44.2</td><td>52.5</td></tr><tr><td>PVT-S [60]</td><td>34.2M</td><td>226B</td><td>40.4</td><td>61.3</td><td>43.0</td><td>25.0</td><td>42.9</td><td>55.7</td></tr><tr><td>Swin-T [36]</td><td>38.5M</td><td>245B</td><td>41.5</td><td>62.1</td><td>44.2</td><td>25.1</td><td>44.9</td><td>55.5</td></tr><tr><td>Twins-SVT-S [5]</td><td>34.3M</td><td>209B</td><td>42.3</td><td>63.4</td><td>45.2</td><td>26.0</td><td>45.5</td><td>56.5</td></tr><tr><td>Twins-PCPVT-S [5]</td><td>34.4M</td><td>226B</td><td>43.0</td><td>64.1</td><td>46.0</td><td>27.5</td><td>46.3</td><td>57.3</td></tr><tr><td>CMT-S (ours)</td><td>44.3M</td><td>231B</td><td>44.3</td><td>65.5</td><td>47.5</td><td>27.1</td><td>48.3</td><td>59.1</td></tr></tbody></table></body></html></div>


<div style="text-align: center;">Table7.Instance segmentation resultson COCOval2017.All models useMask R-CNN15] asbasicrameworkand are traid in $ \text{"}1x\text{"}$ schedule. FLOPs are calculated on $1280\times800$ input.  means the results are from [5]. </div>



<div style="text-align: center;"><html><body><table border="1"><thead><tr><td>Backbone</td><td># Params</td><td># FLOPs</td><td>l $\mathrm{AP}^{\mathrm{box}}$</td><td>$\mathrm{AP_{50}^{box}}$</td><td>= $\mathrm{AP_{75}^{box}}$</td><td>= $\mathrm{A P}^{\mathrm{m a s k}}$</td><td>$\mathrm{A P_{50}^{m a s k}}$</td><td>$\mathrm{A P_{75}^{m a s k}}$</td></tr></thead><tbody><tr><td>ResNet-101 [16]</td><td>63.2M</td><td>336B</td><td>40.0</td><td>60.5</td><td>44.0</td><td>36.1</td><td>57.5</td><td>38.6</td></tr><tr><td>PVT-S [60]</td><td>44.1M</td><td>245B</td><td>40.4</td><td>62.9</td><td>43.8</td><td>37.8</td><td>60.1</td><td>40.3</td></tr><tr><td>ResNeXt-101-32x4d [64]</td><td>62.8M</td><td>340B</td><td>41.9</td><td>62.5</td><td>45.9</td><td>37.5</td><td>59.4</td><td>40.2</td></tr><tr><td>Swin-T† [36]</td><td>47.8M</td><td>264B</td><td>42.2</td><td>64.6</td><td>46.2</td><td>39.1</td><td>61.6</td><td>42.0</td></tr><tr><td>Twins-SVT-S [5]</td><td>44.0M</td><td>228B</td><td>42.7</td><td>65.6</td><td>46.7</td><td>39.6</td><td>62.5</td><td>42.6</td></tr><tr><td>Twins-PCPVT-S [5]</td><td>44.3M</td><td>245B</td><td>42.9</td><td>65.8</td><td>47.1</td><td>40.0</td><td>62.7</td><td>42.9</td></tr><tr><td>CMT-S (ours)</td><td>44.5M</td><td>249B</td><td>44.6</td><td>66.8</td><td>48.9</td><td>40.7</td><td>63.9</td><td>43.4</td></tr></tbody></table></body></html></div>


<div style="text-align: center;">Table8.Trarari elts.Modl-tud wImaeNttdcckpoi.alrm.</div>



<div style="text-align: center;"><html><body><table border="1"><thead><tr><td>Model</td><td># Params</td><td># FLOPs</td><td>CIFAR10</td><td>CIFAR100</td><td>Cars</td><td>Flowers</td><td>Pets</td></tr></thead><tbody><tr><td>ResNet-152† [16]</td><td>58.1M</td><td>11.3B</td><td>97.9%</td><td>87.6%</td><td>92.0%</td><td>97.4%</td><td>94.5%</td></tr><tr><td>Inception-v4† [50]</td><td>41.1M</td><td>16.1B</td><td>97.9%</td><td>87.5%</td><td>93.3%</td><td>98.5%</td><td>93.7%</td></tr><tr><td>EfficientNet-B7↑600 [53]</td><td>64.0M</td><td>37.2B</td><td>98.9%</td><td>91.7%</td><td>94.7%</td><td>98.8%</td><td>95.4%</td></tr><tr><td>ViT-B/16↑384 [10]</td><td>85.8M</td><td>17.6B</td><td>98.1%</td><td>87.1%</td><td></td><td>89.5%</td><td>93.8%</td></tr><tr><td>DeiT-B [57]</td><td>85.8M</td><td>17.6B</td><td>99.1%</td><td>90.8%</td><td>92.1%</td><td>98.4%</td><td></td></tr><tr><td>CeiT-S↑384 [67]</td><td>24.2M</td><td>12.9B</td><td>99.1%</td><td>90.8%</td><td>94.1%</td><td>98.6%</td><td>94.9%</td></tr><tr><td>TNT-S↑384 [14]</td><td>23.8M</td><td>17.3B</td><td>98.7%</td><td>90.1%</td><td></td><td>98.8%</td><td>94.7%</td></tr><tr><td>CMT-S (ours)</td><td>25.1M</td><td>4.04B</td><td>99.2%</td><td>91.7%</td><td>94.4%</td><td>98.7%</td><td>95.2%</td></tr></tbody></table></body></html></div>


with 2.0% mAP. For instance segmentation with Mask RCNN as basic framework, CMT-S surpasses Twins-PCPVTS[5] with 1.7% AP and Twins-SVT-S [5] with 1.9% AP.We also report the inference speed on COCO val2017 with 1280x800 input, CMT-S based RetinaNet and Mask R-CNN achieve 14.8 FPS and 11.2 FPS, respectively.

#### 4.3.2 Other Vision Tasks 

We also evaluate the proposed CMT on five commonly used transfer learning datasets, including CIFAR10 [30],CIFAR100[30],Standford Cars[29], Flowers[4O], and Oxford-IIIT Pets [42] (see Appendix for more details). We fine-tune the ImageNet pretrained models on new datasets following [14,53]. Table 8 shows the corresponding results.CMT-S outperforms other transformer-based models in all datasets with less FLOPs, and achieves comparable performance against Effi cientNet-B7 [53] with 9x less FLOPs,which demonstrates the superiority of CMT architecture.

### 5. Conclusion 

This paper proposes a novel hybrid architecture named CMT for visual recognition and other downstream computer vision tasks such as object detection and instance segmentation, and addresses the limitations of utilizing transformers in a brutal force manner in the field of computer vision. The proposed CMT architectures take advantages of both CNNs and transformers to capture local and global information,promoting the representation ability of the network. In addition, a scaling strategy is proposed to generate a family of CMT variants for different resource constraints. Extensive experiments on ImageNet and other downstream vision tasks demonstrate the effectiveness and superiority of the proposed CMT architecture.



Acknowledgment Chang Xu was supported by the Australian Research Council under Project DP210101859 and the University of Sydney SOAR Prize.


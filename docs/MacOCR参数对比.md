# MacOCR参数对比

结论：

最后还是原来的效果最好，生成的lib

[请至钉钉文档查看附件《libMacOSOCR.dylib》](https://alidocs.dingtalk.com/i/nodes/P7QG4Yx2JpQ0gbl0UYbZ9D7R89dEq3XD?doc_type=wiki_doc&iframeQuery=anchorId%3DX02mcae0b53ll2q9wwxu3c)

文档：[https://developer.apple.com/documentation/vision](https://developer.apple.com/documentation/vision)

不过大多都是swift的代码，而且都写着要求macOS 15.0+（但是这个机子只有12.0）

50

\*说明及尝试：

base：acc\_yes

1.  level
    
    1.  acc代表request.recognitionLevel=VNRequestTextRecognitionLevelAccurate
        

fast代表request.recognitionLevel = VNRequestTextRecognitionLevelFast

2.  yes代表request.usesLanguageCorrection = YES; // 启用语言校正，NO就是不启用
    
3.  observation topCandidates:也尝试过从3->1，并没有明显性能提升
    
4.  request.revision = VNRecognizeTextRequestRevision2，没有明显性能提升
    
5.  输入之前resize，没有明显性能提升
    
6.  对性能影响较大的还是：request.minimumTextHeight （将 `minimumTextHeight` 设置得更高，意味着 Vision 会忽略图像中非常小（可能也包含更多噪声）的文本区域。）相当于牺牲精度换取速度，由0.01->0,05，时间缩短一半，但是相应的部分密集型、小框多的图片的结果就很多都没识别出来。如果要是别的文件的文字不是很多的话可以调高这里
    

| 参数 | 运行时间 | CPU和内存 |
| --- | --- | --- |
| acc\_yes | ![image.png](https://alidocs.oss-cn-zhangjiakou.aliyuncs.com/res/4maOgXbx4146KlWN/img/1aaa43d1-448e-4aa6-9c36-bca613c2fcb0.png) | ![image.png](https://alidocs.oss-cn-zhangjiakou.aliyuncs.com/res/4maOgXbx4146KlWN/img/8c03bb37-dd44-4024-87af-0f0b4cae4c04.png) |
| acc\_no | ![image.png](https://alidocs.oss-cn-zhangjiakou.aliyuncs.com/res/4maOgXbx4146KlWN/img/fef8e41b-e215-470c-b58c-e7b36339b705.png) | ![image.png](https://alidocs.oss-cn-zhangjiakou.aliyuncs.com/res/4maOgXbx4146KlWN/img/7aa14a25-72f5-499b-b266-9297a4710406.png) |
| fast\_yes | ![image.png](https://alidocs.oss-cn-zhangjiakou.aliyuncs.com/res/4maOgXbx4146KlWN/img/2de74fc8-e589-4a36-8014-24f3e635e0bb.png) | ![image.png](https://alidocs.oss-cn-zhangjiakou.aliyuncs.com/res/4maOgXbx4146KlWN/img/dc0cd6d6-110f-4ff2-abf7-e6337af2b034.png) |
| fast\_no | ![image.png](https://alidocs.oss-cn-zhangjiakou.aliyuncs.com/res/4maOgXbx4146KlWN/img/75f3c95b-db42-46c5-a870-58c8cdfc1c73.png) | ![image.png](https://alidocs.oss-cn-zhangjiakou.aliyuncs.com/res/4maOgXbx4146KlWN/img/e8c08c01-a76a-4824-8f19-892a0fba7477.png) |
|  |  |  |

识别结果：

acc\_yes和acc\_no完全一样

fast模式的准确率差太多了

![image.png](https://alidocs.oss-cn-zhangjiakou.aliyuncs.com/res/4maOgXbx4146KlWN/img/49078e65-74ba-4b9f-af20-3ff0234ca39a.png)

![image.png](https://alidocs.oss-cn-zhangjiakou.aliyuncs.com/res/4maOgXbx4146KlWN/img/7f8e29af-cfd9-40bb-ba7b-9ed96a19e353.png)
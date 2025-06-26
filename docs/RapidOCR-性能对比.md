# RapidOCR-性能对比

# 最原始的对比

跑100张 minio上的图 ([http://10.1.2.15:9001/browser/ocrbatchtest](http://10.1.2.15:9001/browser/ocrbatchtest))

| 框架 | 运行时间 | CPU占用率 | GPU占用率 | 内存占用率 |
| --- | --- | --- | --- | --- |
| TBEngine | ![image.png](https://alidocs.oss-cn-zhangjiakou.aliyuncs.com/res/KM7qeobZyZ04klpj/img/1f16d56a-0e66-4bcc-a4bf-e7687ed8b9eb.png) | ![image.png](https://alidocs.oss-cn-zhangjiakou.aliyuncs.com/res/KM7qeobZyZ04klpj/img/eacb2166-6b66-49d1-9d2d-5f7dcabf3fad.png) |  | ![image.png](https://alidocs.oss-cn-zhangjiakou.aliyuncs.com/res/KM7qeobZyZ04klpj/img/62c67cc4-4ba4-4360-a20a-54cdeb841ff6.png) |
| Ncnn-x64 | ![image.png](https://alidocs.oss-cn-zhangjiakou.aliyuncs.com/res/KM7qeobZyZ04klpj/img/78d271f2-4a70-4804-9f9c-968c8bc0dc90.png)<br>时限3s | ![image.png](https://alidocs.oss-cn-zhangjiakou.aliyuncs.com/res/KM7qeobZyZ04klpj/img/fa2fcd7b-a308-4f2a-bff1-d3641bca6777.jpg) |  | ![{496E3EFD-1DDA-4A60-927A-B17B81774DB5}.png](https://alidocs.oss-cn-zhangjiakou.aliyuncs.com/res/KM7qeobZyZ04klpj/img/8f86bce5-f6d0-407e-9983-8d07d92c4e48.jpg)<br>27% |
| Ncnn+vulkan-x64 | ![image.png](https://alidocs.oss-cn-zhangjiakou.aliyuncs.com/res/KM7qeobZyZ04klpj/img/2c8cf5df-a58e-4045-adb4-8eca4a0745cb.png)<br>时限3s | ![a5d9ae5325d6743d12d8ab31ec814f75.png](https://alidocs.oss-cn-zhangjiakou.aliyuncs.com/res/KM7qeobZyZ04klpj/img/0a6198b7-9b1e-4a07-a193-48c35e77272f.jpg) | ![{2AD03808-7E27-4666-AD92-618EFFE29641}.png](https://alidocs.oss-cn-zhangjiakou.aliyuncs.com/res/KM7qeobZyZ04klpj/img/1fb05bfc-7b42-4f7b-b9ec-a3c6e06cbe97.jpg) | ![image.png](https://alidocs.oss-cn-zhangjiakou.aliyuncs.com/res/KM7qeobZyZ04klpj/img/b192ce21-ee70-4ecd-8980-76881d7f9b15.jpg)<br>6% |
| Ncnn-x86 | ![image.png](https://alidocs.oss-cn-zhangjiakou.aliyuncs.com/res/KM7qeobZyZ04klpj/img/4b776844-9127-4c78-b849-70a9aeceb408.png)<br>时限3s | ![image.png](https://alidocs.oss-cn-zhangjiakou.aliyuncs.com/res/KM7qeobZyZ04klpj/img/6cd7b6d7-0e5e-43bd-b5a1-970c8889ec76.png) |  | ![image.png](https://alidocs.oss-cn-zhangjiakou.aliyuncs.com/res/KM7qeobZyZ04klpj/img/028164b4-583f-4805-ac46-a7f3458c2533.png) |
| Ncnn+vulkan-x86 | ![image.png](https://alidocs.oss-cn-zhangjiakou.aliyuncs.com/res/KM7qeobZyZ04klpj/img/55df2c8d-d2ef-4824-bb6d-1987551107ce.png)<br>时限3s | ![image.png](https://alidocs.oss-cn-zhangjiakou.aliyuncs.com/res/KM7qeobZyZ04klpj/img/39e8c1f0-dd11-482c-8dbb-6f3ec338a1bc.png) | ![image.png](https://alidocs.oss-cn-zhangjiakou.aliyuncs.com/res/KM7qeobZyZ04klpj/img/9e1d2b57-ccf6-47a5-b0f5-b5bc9db87bf1.png) | ![image.png](https://alidocs.oss-cn-zhangjiakou.aliyuncs.com/res/KM7qeobZyZ04klpj/img/7942733b-cc8c-4476-85f4-c75be779f279.png) |
| Onnx-x64 | ![image.png](https://alidocs.oss-cn-zhangjiakou.aliyuncs.com/res/KM7qeobZyZ04klpj/img/55b0d3d6-b5d0-4573-ba76-cfe524eca342.jpg)<br>时限3s | ![image.png](https://alidocs.oss-cn-zhangjiakou.aliyuncs.com/res/KM7qeobZyZ04klpj/img/db111650-bb06-47f2-8c20-44dd1d8dc1e4.jpg) |  | ![{4C0EFC8D-4C26-4700-93A1-18AA5B15B724}.png](https://alidocs.oss-cn-zhangjiakou.aliyuncs.com/res/KM7qeobZyZ04klpj/img/664ff8cf-e982-42c8-9919-819a1506d919.jpg)<br>5% |
| Onnx-64 | ![{F398C773-5DF0-4598-B648-7A9294B5D594}.png](https://alidocs.oss-cn-zhangjiakou.aliyuncs.com/res/KM7qeobZyZ04klpj/img/1cfe4117-9d0a-440e-bc0f-501c18d4d03f.jpg)<br>时限5s | ![{86E90D0E-22A9-495B-B48D-1E080D70CE73}.png](https://alidocs.oss-cn-zhangjiakou.aliyuncs.com/res/KM7qeobZyZ04klpj/img/667ce6c2-b226-496c-8e80-332d26df3c62.jpg) |  |  |
| Onnx-x86 | ![image.png](https://alidocs.oss-cn-zhangjiakou.aliyuncs.com/res/KM7qeobZyZ04klpj/img/10917963-1d5d-44ed-9c51-98bf364bd125.png) | ![image.png](https://alidocs.oss-cn-zhangjiakou.aliyuncs.com/res/KM7qeobZyZ04klpj/img/b560abe2-be6b-4b57-8fbe-03e78d701ebb.png) |  | ![image.png](https://alidocs.oss-cn-zhangjiakou.aliyuncs.com/res/KM7qeobZyZ04klpj/img/968adbdb-6f33-4680-9269-157553b339b7.png) |

\*超时的未统计在平均时间中

# 优化内存-EmptyWorkingSet

ncnn+vulkan-x86加入EmptyWorkingSet之后：

（\*注：任务管理器中的内存占用显示的是Working Set）

性能变化：内存⬇，运行时间⬆（但是对时间的影响也不是特别大，最主要的就是工作集减少了）

设置时限3s：

|  | 不加 | 仅DbNet加 | 三个Net都加 |
| --- | --- | --- | --- |
| 占用内存 | ![image.png](https://alidocs.oss-cn-zhangjiakou.aliyuncs.com/res/KM7qeobZyZ04klpj/img/a96c19fe-265c-4f05-82b9-043d09b33625.png) | ![image.png](https://alidocs.oss-cn-zhangjiakou.aliyuncs.com/res/KM7qeobZyZ04klpj/img/a4bd6dc4-c0f8-44b2-a933-f70e24cd1aff.png) | ![image.png](https://alidocs.oss-cn-zhangjiakou.aliyuncs.com/res/KM7qeobZyZ04klpj/img/67c83cdc-a903-43b0-9108-5d27b0aba57a.png) |
| 运行时间 | ![image.png](https://alidocs.oss-cn-zhangjiakou.aliyuncs.com/res/KM7qeobZyZ04klpj/img/6d02189e-72ee-492f-8a0e-f93fb44b65b6.png)<br>![image.png](https://alidocs.oss-cn-zhangjiakou.aliyuncs.com/res/KM7qeobZyZ04klpj/img/0e654a94-2200-48ea-a211-55fd168ba5d5.png) | ![image.png](https://alidocs.oss-cn-zhangjiakou.aliyuncs.com/res/KM7qeobZyZ04klpj/img/0e251929-8031-48d0-ac89-7ff7ba3caec0.png)<br>![image.png](https://alidocs.oss-cn-zhangjiakou.aliyuncs.com/res/KM7qeobZyZ04klpj/img/78005158-9f10-4774-9523-3325f04386ac.png) | ![image.png](https://alidocs.oss-cn-zhangjiakou.aliyuncs.com/res/KM7qeobZyZ04klpj/img/025bb979-7f7d-4e4c-af88-189888c3e1ee.png)<br>![image.png](https://alidocs.oss-cn-zhangjiakou.aliyuncs.com/res/KM7qeobZyZ04klpj/img/27b10da2-f01b-48b2-b0b8-a7783ea46091.png) |

原因：强制Windows将进程的工作集页面移出物理内存，这些页面会被放入页面文件或被标记为可丢弃。当需要再次访问这些页面时，系统需要重新将它们加载回物理内存。

不设置时限

|  | 不加 | 仅DbNet加 | 三个Net都加 |
| --- | --- | --- | --- |
| 占用内存 | ![image.png](https://alidocs.oss-cn-zhangjiakou.aliyuncs.com/res/KM7qeobZyZ04klpj/img/07c08ee6-78cd-477c-8159-ad3f4718562e.png) | ![image.png](https://alidocs.oss-cn-zhangjiakou.aliyuncs.com/res/KM7qeobZyZ04klpj/img/b8e1def2-1d87-4fc3-927b-1ef6f7847c07.png) | ![image.png](https://alidocs.oss-cn-zhangjiakou.aliyuncs.com/res/KM7qeobZyZ04klpj/img/96b9c554-0f3b-4478-9985-54c7cd38baf8.png) |
| 运行时间 | ![image.png](https://alidocs.oss-cn-zhangjiakou.aliyuncs.com/res/KM7qeobZyZ04klpj/img/d2661ef3-9d4b-42e7-96c1-8964758e88b1.png) | ![image.png](https://alidocs.oss-cn-zhangjiakou.aliyuncs.com/res/KM7qeobZyZ04klpj/img/190b8ac8-3c19-409e-9231-4320ee6bb47d.png) | ![image.png](https://alidocs.oss-cn-zhangjiakou.aliyuncs.com/res/KM7qeobZyZ04klpj/img/e3613ef9-9eed-4d68-aad3-18ebce739390.png) |

对比一下原来最少的onnxCPU-x86：

|  | 不加 | DbNet加 |
| --- | --- | --- |
| 占用内存 | ![image.png](https://alidocs.oss-cn-zhangjiakou.aliyuncs.com/res/KM7qeobZyZ04klpj/img/f2a711e0-e50a-4d91-9578-52ec24f1ea33.png) | ![image.png](https://alidocs.oss-cn-zhangjiakou.aliyuncs.com/res/KM7qeobZyZ04klpj/img/7faeabbc-a826-44c1-827b-66d13c5d2aba.png) |
| 运行时间 | ![image.png](https://alidocs.oss-cn-zhangjiakou.aliyuncs.com/res/KM7qeobZyZ04klpj/img/b95b34cc-2fe0-487d-99e4-d6f8afdbc89a.png) | ![image.png](https://alidocs.oss-cn-zhangjiakou.aliyuncs.com/res/KM7qeobZyZ04klpj/img/24c32753-f22f-4507-b589-3ffff548cda9.png) |

# Mac对比

| 方法 | 运行时间 | CPU和内存 |
| --- | --- | --- |
| ncnn，50 | ![image.png](https://alidocs.oss-cn-zhangjiakou.aliyuncs.com/res/KM7qeobZyZ04klpj/img/438122e1-c182-4c01-afee-5a91ffa0b1c5.png) | ![image.png](https://alidocs.oss-cn-zhangjiakou.aliyuncs.com/res/KM7qeobZyZ04klpj/img/67c8e0ed-cd7c-4d42-b4da-18bc3e5b9f63.png) |
| apple vision,50 | ![image.png](https://alidocs.oss-cn-zhangjiakou.aliyuncs.com/res/KM7qeobZyZ04klpj/img/726b6b63-9c5a-48e0-a791-4558e4c245a4.png) | ![image.png](https://alidocs.oss-cn-zhangjiakou.aliyuncs.com/res/KM7qeobZyZ04klpj/img/74e615a4-6fa9-41bd-adca-2fa868400b79.png) |
| onnx，50 | ![image.png](https://alidocs.oss-cn-zhangjiakou.aliyuncs.com/res/KM7qeobZyZ04klpj/img/8d6f7de5-e904-4302-aba0-abe24dec36b8.png) | ![image.png](https://alidocs.oss-cn-zhangjiakou.aliyuncs.com/res/KM7qeobZyZ04klpj/img/a785fecd-2713-4c92-b3cf-41343fe169e1.png) |
|  |  |  |

# ppocrv5

[RapidOCR · 模型库](https://www.modelscope.cn/models/RapidAI/RapidOCR/files)

mac可以运行，win不行

但还是存在问题：

1.  v5识别时间长且内容奇怪：
    

![image.png](https://alidocs.oss-cn-zhangjiakou.aliyuncs.com/res/KM7qeobZyZ04klpj/img/dc471927-1a2a-4019-94fb-db9e7fe5bca8.png)

已解决：[https://github.com/RapidAI/RapidOCR/issues/478](https://github.com/RapidAI/RapidOCR/issues/478)，一个就是Onnxruntime版本的问题（原来的版本太低了），一个就是keys要更新。但是采用这个新模型跑出来的结果就是特别特别慢

这是采用v5的mac跑出来一张的速度：（左边是v3，右边是v5）

![image.png](https://alidocs.oss-cn-zhangjiakou.aliyuncs.com/res/KM7qeobZyZ04klpj/img/b92b79ac-15f7-46d3-8a03-c9581aadbcfd.png)

50张（左边是v3，右边是v5）

![image.png](https://alidocs.oss-cn-zhangjiakou.aliyuncs.com/res/KM7qeobZyZ04klpj/img/b2e01897-f553-4058-8447-b687a69bd36d.png)

上面的都是mac的

# ncnn vulkan x86 最新优化

\*50，[尝试过这里的方法](https://github.com/Tencent/ncnn/wiki/faq#%E5%A6%82%E4%BD%95%E8%B7%91%E5%BE%97%E6%9B%B4%E5%BF%AB%E5%86%85%E5%AD%98%E5%8D%A0%E7%94%A8%E6%9B%B4%E5%B0%91%E5%BA%93%E4%BD%93%E7%A7%AF%E6%9B%B4%E5%B0%8F)

v0：原本的（\*Tips：AngleNet不使用vulkan综合性能更好）

v1：加入emptyworkingset，工作集内存下降了约90%

v2：main.cpp的numThread由4改为1，cpu占比下降约75%，其他指标基本不变

v3：加入openmp，微小的变化（不是很稳定，有时效果也和v2差不多），开启int8（三个Net内），调整别的参数也差不多，没有更好的优化方向了暂时，

v4：用ncnnoptimize对cls、det、rec模型进行优化，时间稍微缩短了一点

v5（失败）：[参考](https://github.com/Tencent/ncnn/blob/master/docs/how-to-use-and-FAQ/quantized-int8-inference.md)对模型进行int8量化，先ncnn2table生成量化表，再利用量化表生成int8模型->结果识别出来的结果全部是乱的而且还慢了好多。可能是table提供的图片太少且不具备代表性。尝试用大型数据集更换一下重新生成table（还在训练/生成的比较慢，且不保证数据集适合）

目前选取的数据集（ICDAR2019-ArT）不好，det和rec量化出来的结果后面都是0。数据集就直接用官方的把：[ppocr官方数据集](https://paddlepaddle.github.io/PaddleOCR/main/version3.x/module_usage/text_recognition.html#_5)，maybe是ncnn版本的问题，我尝试一下用项目里的bin来做转换，问题依旧

直接ncnn2int8，不用table的结果。GPU 驱动只支持 1 个 compute queue，所以开启了batch也还是串行；且ncnn本来支持的也只是1输入，batch这条也没走通

将多个框合并后一起识别，时间变化不大

![image.png](https://alidocs.oss-cn-zhangjiakou.aliyuncs.com/res/KM7qeobZyZ04klpj/img/fff17be1-d172-4da2-831b-c10ebcad86cb.png)

![image.png](https://alidocs.oss-cn-zhangjiakou.aliyuncs.com/res/KM7qeobZyZ04klpj/img/bb3097c3-bc65-4f2d-9098-12a6e4d205b6.png)

运行时间其实都差不多）其他指标几点的浮动都是合理范围

| 版本 | 运行时间 | 平均cpu | 平均gpu | 平均内存 |
| --- | --- | --- | --- | --- |
| v0 | ![image.png](https://alidocs.oss-cn-zhangjiakou.aliyuncs.com/res/KM7qeobZyZ04klpj/img/0e611e18-440b-4360-8ef1-1c145ef0427f.png) | ![image.png](https://alidocs.oss-cn-zhangjiakou.aliyuncs.com/res/KM7qeobZyZ04klpj/img/b008f7f0-138a-4080-b4d5-d4babe1bdbe1.png) | ![image.png](https://alidocs.oss-cn-zhangjiakou.aliyuncs.com/res/KM7qeobZyZ04klpj/img/3129dd49-4bfe-47d9-b694-af67cafd3094.png) | ![image.png](https://alidocs.oss-cn-zhangjiakou.aliyuncs.com/res/KM7qeobZyZ04klpj/img/2cbf6719-5d3a-4586-8a5d-db9a0e09d78c.png) |
| v1 | ![image.png](https://alidocs.oss-cn-zhangjiakou.aliyuncs.com/res/KM7qeobZyZ04klpj/img/863c9695-4b7c-4f9c-9f36-ebe983fd1186.png) | ![image.png](https://alidocs.oss-cn-zhangjiakou.aliyuncs.com/res/KM7qeobZyZ04klpj/img/3d3f516a-1aa5-434a-ae1f-8e256ee652de.png) | ![image.png](https://alidocs.oss-cn-zhangjiakou.aliyuncs.com/res/KM7qeobZyZ04klpj/img/c30331ba-e38c-414c-9827-7c95c1d5767a.png) | ![image.png](https://alidocs.oss-cn-zhangjiakou.aliyuncs.com/res/KM7qeobZyZ04klpj/img/f8db05ba-5c3e-4169-b5a9-641b0352cef6.png) |
| v2 | ![image.png](https://alidocs.oss-cn-zhangjiakou.aliyuncs.com/res/KM7qeobZyZ04klpj/img/784a1401-482a-423e-8ca2-b0d8bbdb5283.png) | ![image.png](https://alidocs.oss-cn-zhangjiakou.aliyuncs.com/res/KM7qeobZyZ04klpj/img/40df585e-2cbd-4e76-956a-d1b46e83d3ce.png) | ![image.png](https://alidocs.oss-cn-zhangjiakou.aliyuncs.com/res/KM7qeobZyZ04klpj/img/9e177602-44fc-4c16-9935-69e2269cf29a.png) | ![image.png](https://alidocs.oss-cn-zhangjiakou.aliyuncs.com/res/KM7qeobZyZ04klpj/img/2b25d1dc-bc9f-493c-a82b-b6e79617acd1.png) |
| v3 | ![image.png](https://alidocs.oss-cn-zhangjiakou.aliyuncs.com/res/KM7qeobZyZ04klpj/img/c6fdd3ab-6b6c-41b2-831d-4fc89908f6db.png) | ![image.png](https://alidocs.oss-cn-zhangjiakou.aliyuncs.com/res/KM7qeobZyZ04klpj/img/623f4825-78ac-4cc9-8bd4-cb7e3e628a6d.png) | ![image.png](https://alidocs.oss-cn-zhangjiakou.aliyuncs.com/res/KM7qeobZyZ04klpj/img/f5cb7d14-6e4c-4ec3-b37d-b3b3604ba0d2.png) | ![image.png](https://alidocs.oss-cn-zhangjiakou.aliyuncs.com/res/KM7qeobZyZ04klpj/img/bbdcb90d-b8e0-4e30-93e6-b5ab3890ecba.png) |
| v4 | ![image.png](https://alidocs.oss-cn-zhangjiakou.aliyuncs.com/res/KM7qeobZyZ04klpj/img/c13d447e-b617-433c-a22b-d2ac1d32847c.png) | ![image.png](https://alidocs.oss-cn-zhangjiakou.aliyuncs.com/res/KM7qeobZyZ04klpj/img/baeb3398-c5d8-4722-b5f1-dba38fe81f91.png) | ![image.png](https://alidocs.oss-cn-zhangjiakou.aliyuncs.com/res/KM7qeobZyZ04klpj/img/26a115f3-eeb1-40bd-9bd8-9d66db6125d3.png) | ![image.png](https://alidocs.oss-cn-zhangjiakou.aliyuncs.com/res/KM7qeobZyZ04klpj/img/ae6a4864-57e1-473f-8169-371ff11c53e4.png) |

所以最终收敛在运行时间均1.4s，cpu均4%，gpu均50%，工作集内存均25MB

### 从模型下手的尝试

1.  尝试用ppocrV5
    

尝试将ppocrv5由onnx转成ncnn，但是第三层次open failed

虽然产生了文件但是也不完整没法跑出来，提了issue未回复

2.  尝试用ncnnoptimize（模型路径：C:\Users\cting\Desktop\pic\ncnnmodelsUP）
    

直接优化的化层数会不匹配（注意用x86的）

试了一下ncnnoptimize的x86版本能成功跑出来，模型在：C:\Users\cting\Desktop\pic\ncnn1

3.  尝试用ncnn2int8（模型路径：C:\Users\cting\Desktop\pic\ncnnInt8）
    

存一下

![image.png](https://alidocs.oss-cn-zhangjiakou.aliyuncs.com/res/KM7qeobZyZ04klpj/img/81bdaaf2-b83b-4b21-ab93-500cfbb57a8e.png)

# OcrLiteNcnn

[https://github.com/benjaminwan/OcrLiteNcnn](https://github.com/benjaminwan/OcrLiteNcnn)

vulkan win32

gpu：0 -1 -1 （只有dbNet用gpu最快）

cpuThread改为1

加上emptyworkingset

![image.png](https://alidocs.oss-cn-zhangjiakou.aliyuncs.com/res/KM7qeobZyZ04klpj/img/f8a3d730-11f5-401a-9a6c-33adcd367aa7.png)

平均cpu：9%

平均gpu：12%

平均内存：工作集25MB
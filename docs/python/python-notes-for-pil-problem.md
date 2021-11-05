# Python3 PIL库问题：ImageChops.difference返回None


遇到一个关于python PIL库的问题：在python3中，两张明显不同的图片，使用`ImageChops.difference` 方法计算他们的差异，diff.getbbox()返回值为None，相同的代码在python2中运行就没有问题：

```python
im_source_obj = Image.open(self.im_source_path)
im_target_obj = Image.open(self.im_target_path)
diff = ImageChops.difference(im_source_obj, im_target_obj)
if diff.getbbox() is None:
	print("图片相同")
```
我的python3版本为 Python 3.7.6，Pillow== 8.4.0；python2版本为 Python 2.7.16，Pillow == 6.2.2 。

解决方案：

stackoverflow上有类似的问题：[https://stackoverflow.com/questions/61812374/imagechops-difference-not-working-with-simple-png-images](https://stackoverflow.com/questions/61812374/imagechops-difference-not-working-with-simple-png-images)

转换为RGB通道：
```python
im_source_obj = Image.open(self.im_source_path).convert('RGB')
im_target_obj = Image.open(self.im_target_path).convert('RGB')
print(im_source_obj.mode)
diff = ImageChops.difference(im_source_obj, im_target_obj)
if diff.getbbox() is None:
	print("图片相同")
```

Image.open() 方法默认返回的是RGBA模式，多一个alpha通道，用来记录图像的透明度。其实python2也返回的是RGBA模式，不知道具体是什么原因导致python3中需要转换为RGB通道，也可能是版本问题。


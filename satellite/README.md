# 这个代码用于给出地球上某个地点（经纬度），不同时间能见到的starlink卫星ID
#自己新建虚拟环境，python版本用3.8
#自己安装pip install numpy
#自己安装pip install skyfield
#track.py里面的tle文件下载网址需要更新,https://celestrak.org/NORAD/elements/
#在这个网址找到starlink的，换成最新时间的网址，你自己的地点经纬度写好
#运行的时候运行进入code文件夹，运行find_satellite.py，这个会调用track.py
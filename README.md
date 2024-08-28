# DGLAB-CS2

**联动郊狼与cs2！**

## 功能列表

- [x] 强度随血量变化
- [ ] 强度叠加，死亡时增加强度，击杀降低强度
- [ ] 受击时同步电击，不受击不电击

## 前置要求

1. 本项目仅适用于郊狼2.0，作者没钱买3.0所以没写3.0的适配
2. 本项目通过蓝牙直接与郊狼连接，因此需要你的电脑有蓝牙功能

## 教程

1. 在release下载最新版本
2. 将压缩包中的cfg文件放入 `<你的steam路径>\steamapps\common\Counter-Strike Global Offensive\game\csgo\cfg`
3. 根据说明，修改 `config.toml`
4. 打开郊狼，并关闭再打开一次你的电脑的蓝牙开关
5. 打开游戏
6. 运行 `main.exe` 

## 常见问题

- 如果遇到郊狼强度有延迟/与当前游戏内血量不一致的情况，请关闭再开启一次电脑的蓝牙开关，然后再打开软件进行连接
- 如果遇到连接失败，请先重启郊狼，然后关闭并重新打开软件

## 配置说明

|配置名称|描述|
|---|---|
|debug|debug输出开关|
|base_strength|郊狼的基础强度(int)，范围 1-200|
|strength_per_hp|每减少一滴血量将增加多少强度，越大越强，建议范围 0.2-1|
|keep_strength_while_not_injured|是否在满血时仍然电击，设置为 false 则将在满血时不放电|

## Credit

Huge thanks to repo [CSGO-GSI](https://github.com/mdarvanaghi/CSGO-GSI) by [mdarvanaghi](https://github.com/mdarvanaghi).

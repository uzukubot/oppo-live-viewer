# 🚀 OPPO Live Photo Viewer - 快速开始

## 一键打包（需要Python和pip）

```bash
cd /home/yezichao/.openclaw/workspace/oppo-live-viewer
./build_simple.sh
```

完成后双击 `dist/OPPO-Live-Viewer` 运行！

---

## 📋 检查清单

打包前确保：

- [ ] Python 3.9+ 已安装
- [ ] pip 可用 (`pip --version`)
- [ ] 有足够的磁盘空间（约500MB）

---

## 🔧 如果打包失败

### 情况1: 没有pip
```bash
sudo apt-get install python3-pip
```

### 情况2: 缺少系统依赖
```bash
sudo ./install_and_build.sh
```

### 情况3: 手动安装
查看 `PACKAGE_GUIDE.md` 获取详细步骤

---

## ✅ 打包完成后

```bash
cd dist
./OPPO-Live-Viewer
```

或直接在文件管理器中双击！

---

## 📝 详细文档

- `README.md` - 完整使用说明
- `PACKAGE_GUIDE.md` - 详细打包指南
- `PROJECT_SUMMARY.md` - 项目总结

---

## 🐛 遇到问题？

1. 检查Python版本: `python3 --version`
2. 查看错误日志
3. 参考 `PACKAGE_GUIDE.md` 故障排除部分

---

**简单到爆！** 😎

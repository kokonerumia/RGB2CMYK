# RGB to CMYK Converter

RGB色空間からCMYK色空間への変換を行うPythonアプリケーションです。特にAdobe Illustratorでの使用を想定し、Japan Color 2001 Coatedのカラープロファイルに基づいて変換を行います。

## 特徴

- Japan Color 2001 Coatedプロファイルを使用したカラー変換
- リアルタイムのカラープレビュー
- RGBの数値入力とスライダー操作に対応
- CMYKの最適化機能

## 必要要件

- Python 3.x
- PyQt6
- Pillow (PIL)
- numpy

## インストール

```bash
# 必要なパッケージのインストール
pip install PyQt6 Pillow numpy
```

## 使用方法

```bash
python color_converter_gui.py
```

### GUI操作方法

1. RGBの値を入力
   - スライダーで調整
   - 直接数値を入力（0-255）

2. CMYKの確認
   - 自動的にCMYK値が計算されます
   - 「CMYKを最適化」ボタンで最適な変換値を取得

## 技術的詳細

### カラー変換の仕組み

- RGBからCMYKへの変換にはPillowのImageCmsモジュールを使用
- Japan Color 2001 Coatedのカラープロファイルを適用
- 色域マッピングにはRelative Colorimetricレンダリングインテントを使用

### 制限事項

- RGBの色域はCMYKより広いため、完全な色の再現が難しい場合があります
- 特に鮮やかな青色などの再現に制限があります
- Japan Color 2001 Coatedの仕様により、インクの総使用量は350%までに制限されます

### ファイル構成

- `color_converter_gui.py`: GUIアプリケーションのメインファイル
- `rgb_to_cmyk.py`: カラー変換のコアロジック
- `README.md`: ドキュメント

## 参考文献

- [Japan Color 2001 Coated](https://www.japancolor.jp/standard.html)
- [PIL (Python Imaging Library)](https://pillow.readthedocs.io/)
- [PyQt6 Documentation](https://www.riverbankcomputing.com/static/Docs/PyQt6/)

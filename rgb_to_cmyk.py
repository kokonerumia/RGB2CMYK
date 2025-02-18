from PIL import Image, ImageCms
import numpy as np
import os

def find_icc_profile():
    """
    Japan Color 2001 CoatedのICCプロファイルを探す関数
    """
    possible_paths = [
        # Adobe標準のパス
        "/Library/Application Support/Adobe/Color/Profiles/Recommended/JapanColor2001Coated.icc",
        # システムのパス
        "/System/Library/ColorSync/Profiles/JapanColor2001Coated.icc",
        # カレントディレクトリ
        "JapanColor2001Coated.icc",
        # プロファイルディレクトリ
        "profiles/JapanColor2001Coated.icc"
    ]
    
    for path in possible_paths:
        if os.path.exists(path):
            return path
    
    # プロファイルが見つからない場合はデフォルトのCMYKプロファイルを使用
    return ImageCms.createProfile(
        "CMYK",
        colorSpace="CMYK",
        connectionSpace="Lab"
    )

def get_transform():
    """
    RGB→CMYK変換のためのtransformを取得する関数
    """
    # sRGBプロファイル
    srgb_profile = ImageCms.createProfile("sRGB")
    
    # CMYK (Japan Color 2001 Coated) プロファイル
    try:
        jc_profile_path = find_icc_profile()
        if isinstance(jc_profile_path, str):
            cmyk_profile = ImageCms.getOpenProfile(jc_profile_path)
        else:
            cmyk_profile = jc_profile_path
            print("警告: Japan Color 2001 Coatedプロファイルが見つかりません。デフォルトのCMYKプロファイルを使用します。")
    except Exception as e:
        print(f"警告: プロファイルの読み込みに失敗しました: {e}")
        cmyk_profile = ImageCms.createProfile(
            "CMYK",
            colorSpace="CMYK",
            connectionSpace="Lab"
        )
    
    # RGB→CMYK変換のtransformを作成
    transform = ImageCms.buildTransform(
        srgb_profile,
        cmyk_profile,
        "RGB",
        "CMYK",
        renderingIntent=ImageCms.Intent.RELATIVE_COLORIMETRIC
    )
    
    return transform

def get_reverse_transform():
    """
    CMYK→RGB変換のためのtransformを取得する関数
    """
    # sRGBプロファイル
    srgb_profile = ImageCms.createProfile("sRGB")
    
    # CMYK (Japan Color 2001 Coated) プロファイル
    try:
        jc_profile_path = find_icc_profile()
        if isinstance(jc_profile_path, str):
            cmyk_profile = ImageCms.getOpenProfile(jc_profile_path)
        else:
            cmyk_profile = jc_profile_path
    except Exception as e:
        print(f"警告: プロファイルの読み込みに失敗しました: {e}")
        cmyk_profile = ImageCms.createProfile(
            "CMYK",
            colorSpace="CMYK",
            connectionSpace="Lab"
        )
    
    # CMYK→RGB変換のtransformを作成
    transform = ImageCms.buildTransform(
        cmyk_profile,
        srgb_profile,
        "CMYK",
        "RGB",
        renderingIntent=ImageCms.Intent.RELATIVE_COLORIMETRIC
    )
    
    return transform

def rgb_to_cmyk(r, g, b):
    """
    RGBからCMYKへの変換を行う関数
    Japan Color 2001 Coated プロファイルを使用
    
    Parameters:
    r, g, b (int): 0-255の範囲のRGB値
    
    Returns:
    tuple: (c, m, y, k) の値（0-100の範囲）
    """
    # 1x1のRGB画像を作成
    rgb_image = Image.new('RGB', (1, 1), (r, g, b))
    
    # 変換を適用
    transform = get_transform()
    cmyk_image = ImageCms.applyTransform(rgb_image, transform)
    
    # CMYK値を取得（0-255の範囲）
    c, m, y, k = cmyk_image.getpixel((0, 0))
    
    # 0-100の範囲に変換
    c = (c / 255.0) * 100
    m = (m / 255.0) * 100
    y = (y / 255.0) * 100
    k = (k / 255.0) * 100
    
    return (c, m, y, k)

def cmyk_to_rgb(c, m, y, k):
    """
    CMYKからRGBへの変換を行う関数
    Japan Color 2001 Coated プロファイルを使用
    
    Parameters:
    c, m, y, k (float): 0-100の範囲のCMYK値
    
    Returns:
    tuple: (r, g, b) の値（0-255の範囲）
    """
    # CMYK値を0-255の範囲に変換
    c = int((c / 100.0) * 255)
    m = int((m / 100.0) * 255)
    y = int((y / 100.0) * 255)
    k = int((k / 100.0) * 255)
    
    # 1x1のCMYK画像を作成
    cmyk_image = Image.new('CMYK', (1, 1), (c, m, y, k))
    
    # 変換を適用
    transform = get_reverse_transform()
    rgb_image = ImageCms.applyTransform(cmyk_image, transform)
    
    # RGB値を取得
    r, g, b = rgb_image.getpixel((0, 0))
    
    return (r, g, b)

def process_color(rgb_color):
    """
    RGB色をCMYKに変換して結果を表示する関数
    
    Parameters:
    rgb_color (tuple): (R, G, B)の形式のタプル（値は0-255）
    """
    r, g, b = rgb_color
    c, m, y, k = rgb_to_cmyk(r, g, b)
    print(f"RGB ({r}, {g}, {b}) -> CMYK ({c:.1f}%, {m:.1f}%, {y:.1f}%, {k:.1f}%)")
    return (c, m, y, k)

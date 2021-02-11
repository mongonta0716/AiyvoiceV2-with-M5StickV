# aiyvoicev2-with-m5stickv
Extend the functionality of GoogleAIYVoicekitV2 with voice recognition of the M5StickV.

# 概要(Overview)
　
GoogleAIYVoicekitV2とマイク付きのM5StickVをExt.IO Unitで連携することによりウェイクワードでの起動機能を追加します。

# 開発環境(Develop Environment)
　
Speech Recognizerを使用するため、Sipeedから正式にリリースされているファームウェアでは動きません。importエラーが起きます。
- MaixPy IDE v0.2.5
- firmware 0.6.2（ビルド済みのものを添付しています。）

※ ファームウェアはM5StickV用です。

## ファームウェアのビルド方法

[M5StickVのファームウェアビルド手順](https://raspberrypi.mongonta.com/howto-build-firmware-of-m5stickv/)を参照してください。（日本語のみ）

# 対応機種
## GoogleAIYVoicekitV2
VoicekitV1はGPIOが異なるので使用できません。

## M5StickV（マイク搭載バージョンのみ）
ファームウェアを書き換えると、M5StickVの電源ボタンの挙動が変わるので注意してください。
- 電源ON：電源ボタンを短く２回押す
- 電源OFF：電源ボタンを２秒以上長押し

## Ext.IO Unit
M5StickVのGrove互換ポート（HY-2.0-4P）を拡張するために利用します。

# 使い方(Usage)

詳しくは下記のリンクを参照してください。

# 参考にしたソース
Sipeed社のMaix_Scriptsにある[isolated_word.py](https://github.com/sipeed/MaixPy_scripts/blob/master/multimedia/speech_recognizer/isolated_word.py)を参考に作成しました。
Google社の[aiyprojects-raspbian](https://github.com/google/aiyprojects-raspbian)の[assistant_grpc_demo.py](https://github.com/google/aiyprojects-raspbian/tree/aiyprojects/src/examples/voice)を参考に作成しました。

# LICENSE
[MIT](LICENSE)

# Author
[Takao Akaki](https://github.com/mongonta0716)

from django.core.exceptions import ValidationError
import re

# パスワードの要件を決めるクラス
class PasswordValidator:
    # パスワードのチェックを行うメソッド
    #   問題なければ何もしない
    #   問題があればValidationErrorを発生させる
    def validate(self, password, user=None):
        # passwordが英大文字小文字数字を含む8文字以上でないかどうか
        # =>正規表現で調べる！
        if not re.match("\A(?=.*?[a-z])(?=.*?[A-Z])(?=.*?\d)[a-zA-Z\d]{8,100}\Z", password):
            raise ValidationError(
                "パスワードは英大文字小文字数字を含む8文字以上を入力してください"
            )

    # ヘルプ用のテキスト
    def get_help_text(self):
        return "パスワードは英大文字小文字数字を含む8文字以上を入力してください"

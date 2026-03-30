package ui;

import javax.swing.JOptionPane;
import checker.CommitMessageChecker;

public class CommitDialog {
    public static void main(String[] args) {
        String commitMessage = JOptionPane.showInputDialog(
                null,
                "أدخل رسالة الالتزام:",
                "فحص الالتزام",
                JOptionPane.PLAIN_MESSAGE
        );

        if (commitMessage == null) {
            return;
        }

        boolean isValid = CommitMessageChecker.validate(commitMessage);
        String validationMessage = isValid
                ? "✅ الرسالة صحيحة!"
                : "❌ الرسالة غير صحيحة. تأكد من القواعد.";

        JOptionPane.showMessageDialog(
                null,
                validationMessage,
                "نتيجة التحقق",
                JOptionPane.INFORMATION_MESSAGE
        );
    }
}

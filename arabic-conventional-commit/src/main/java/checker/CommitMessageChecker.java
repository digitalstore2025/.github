package checker;

import java.util.regex.Pattern;

public class CommitMessageChecker {
    public static final int MAX_COMMIT_MESSAGE_LENGTH = 72;
    private static final Pattern COMMIT_PATTERN = Pattern.compile(
            "^(?:تحسين|إصلاح|توثيق|تنسيق|اختبار|تحديث): .+$"
    );

    public static boolean validate(String commitMessage) {
        if (commitMessage == null) {
            return false;
        }
        if (commitMessage.length() > MAX_COMMIT_MESSAGE_LENGTH) {
            return false;
        }
        return COMMIT_PATTERN.matcher(commitMessage).matches();
    }
}

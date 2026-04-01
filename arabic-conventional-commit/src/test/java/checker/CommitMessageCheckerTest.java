package checker;

import org.junit.jupiter.api.Test;

import static org.junit.jupiter.api.Assertions.assertFalse;
import static org.junit.jupiter.api.Assertions.assertTrue;

class CommitMessageCheckerTest {

    @Test
    void acceptsValidArabicTypes() {
        assertTrue(CommitMessageChecker.validate("تحسين: إضافة تحسينات"));
        assertTrue(CommitMessageChecker.validate("إصلاح: إصلاح خطأ واجهة"));
        int availableLength = CommitMessageChecker.MAX_COMMIT_MESSAGE_LENGTH - "تحسين: ".length();
        assertTrue(CommitMessageChecker.validate("تحسين: " + "أ".repeat(availableLength)));
    }

    @Test
    void rejectsInvalidPrefixOrFormat() {
        assertFalse(CommitMessageChecker.validate("feat: missing arabic keyword"));
        assertFalse(CommitMessageChecker.validate("إصلاح - لا يوجد نقطتان"));
        assertFalse(CommitMessageChecker.validate(null));
    }

    @Test
    void rejectsTooLongMessages() {
        int longBodyLength = CommitMessageChecker.MAX_COMMIT_MESSAGE_LENGTH - "تحسين: ".length() + 1;
        String overLimit = "أ".repeat(longBodyLength);
        assertFalse(CommitMessageChecker.validate("تحسين: " + overLimit));
    }
}

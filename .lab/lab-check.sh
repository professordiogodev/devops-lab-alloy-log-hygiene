#!/usr/bin/env bash
rc=0
grep -q 'TODO' PRIVACY.md && { echo "- ❌ PRIVACY.md still has TODO"; rc=1; } || echo "- ✅ PRIVACY.md is filled in"
grep -q 'stage.replace' alloy/config.alloy && grep -q 'stage.multiline' alloy/config.alloy && grep -q 'stage.drop' alloy/config.alloy && echo "- ✅ the pipeline has replace, multiline and drop" || { echo "- ❌ alloy/config.alloy is missing stage.replace, stage.multiline or stage.drop"; rc=1; }
grep -qE '^ALL CHECKS PASSED \(' SUBMISSION.md && echo "- ✅ SUBMISSION.md shows ALL CHECKS PASSED" || { echo "- ❌ paste the verify.sh output ('ALL CHECKS PASSED') into SUBMISSION.md"; rc=1; }
exit $rc

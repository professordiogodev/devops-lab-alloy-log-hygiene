# Submission

Fork URL: <!-- paste the URL of your fork here -->

## Files to commit

- [ ] `alloy/config.alloy`: your pipeline
- [ ] `PRIVACY.md`: what you redacted and why

## Questions

Answer in your own words. Where a question asks for output, paste it in a code block.

### Q1. Paste your Alloy pipeline. Describe the journey of one log line through your stages, in order. Why does the order of the stages matter (for example, `multiline` before `json`, redaction before labels)?

**Your answer:**

<!-- replace this line with your answer -->

### Q2. Which three kinds of sensitive data did you find in the logs? For each, paste the regular expression you used and one example before and after. What kinds of personal data could still slip through your patterns, and what is the better fix at the source?

**Your answer:**

<!-- replace this line with your answer -->

### Q3. Show what you dropped (health checks, debug) and say how much storage it saved: compare lines per minute in the container with lines per minute stored in Loki. Is dropping `debug` always right? What would you keep for an incident?

**Your answer:**

<!-- replace this line with your answer -->

### Q4. Which labels does a stored line carry, and which did you refuse to make labels? Explain high cardinality in your own words and give one label that would have made Loki slow or expensive.

**Your answer:**

<!-- replace this line with your answer -->

### Q5. A stack trace is 12 lines. What does the log store do with them by default, why is that a problem when you search for the exception, and what did you do about it?

**Your answer:**

<!-- replace this line with your answer -->

### Q6. GDPR says people can ask you to delete their data. Why is it nearly impossible to delete one customer's e-mail from an immutable log store after the fact, and what does that say about WHERE in the pipeline the redaction must happen?

**Your answer:**

<!-- replace this line with your answer -->

### Q7. Paste the output of `./verify.sh`. It must end with **ALL CHECKS PASSED**.

**Your answer:**

<!-- replace this line with your answer -->

### Q8. **Tear down.** Paste the output of `./verify-teardown.sh`. It must end with **TEARDOWN VERIFIED**.

**Your answer:**

<!-- replace this line with your answer -->

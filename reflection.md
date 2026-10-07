# 💭 Reflection: Game Glitch Investigator

Answer each question in 3 to 5 sentences. Be specific and honest about what actually happened while you worked. This is about your process, not trying to sound perfect.

## 1. What was broken when you started?

- What did the game look like the first time you ran it?
It was largely broken, but the objective of the game was clear. The first thing I noticed were the inconsistincies in the difficulty scaling. For example, the easy mode had too few attempts, the normal mode had too wide a range of numbers to guess from. When I tried a number, I checked the debugger and the hints suggested that I go even lower for undershot guesses. This did not make sense and was another immediate red flag to debug. 
- List at least two concrete bugs you noticed at the start  
  (for example: "the hints were backwards"). The first bug I noticed was that the range of numbers to guess from for the normal difficulty was too big (1 to 100) and the range of numbers for the hard difficulty was too small ( 1 to 50). This did not make sense and should be reversed. Moreover, the normal difficulty got 8 attempts whereas the easy difficulty got only 6. Again, this did not make sense for the nature of the game and should have been the reverse.

**Bug Reproduction Log**

Document at least 3 bugs you found. Add rows as needed.

| Input | Expected Behavior | Actual Behavior | Console Output / Error |
|-------|-------------------|-----------------|------------------------|
|1 | Too Low, Go Higher|Too Low, Go Lower| Go Lower hint for an low num|
| 51 | Too High, Go Lower | Too High, Go Higher | Go Higher hint for a high num |
|Normal Difficulty | Guess a number between 1 and 50  | Guess a number between 1 and 100| Guess a number between 1 and 100 was hardcoded regardless of input and changes in number range |

---

## 2. How did you use AI as a teammate?

- Which AI tools did you use on this project (for example: ChatGPT, Gemini, Copilot)?

 I only used Claude Code as an AI tool assistant. At first I was using opus because that was the default and recommended model, but I noticed extremely high token usage for relatively small fixes. Then I checked the course slides that suggested I use sonnet instead of Opus so after the first bug was identified and fixed, I changed over to sonnet.

- Give one example of an AI suggestion that was correct (including what the AI suggested and how you verified the result).

One suggestion it gave was to remove the even-numbered guess check and the fallback "catch" logic in check_guess. I asked it to explain why it should be removed, and what an example of a incorrect behavior would look like (trace it). Then I traced the example on my own and came to the same conclusion as the AI that it would result in incorrect behavior, that is, that a TypeError would default to string comparison where something like a guess of 10 and a secret of 9 would result in a hint to go HIGHER instead of lower because of how Python compares strings character by character. So to remove this headache, it suggested removed the even-numbered attempt check and the try-catch block that handled the case where the TypeError occurs.

- Give one example of an AI suggestion you did not accept as written (including what the AI suggested, why you rejected or changed it, and how you verified your version). It does not have to be a suggestion that was wrong: over-engineered, out of scope, harder to read, or a poor fit for this codebase all count.

 After removing the even-numbered check, I prompted Claude Code to write test cases to verify the functionality of the new changes. It still wrote test cases for the old (now removed) logic that checked how string comparison of numbers works. I think it may have done this as an education resource, but it was not necessary and out of scope of the project now that the relevant logic was removed from the codebase. Therefore, I told Claude Code to remove it as it was now out-of-scope:

Please see the examples of out of scope tests: 
@pytest.mark.parametrize(
    "guess, secret, expected",
    [
        (9, 10, "Too Low"),     # "9" > "10" as strings, but 9 < 10 numerically
        (10, 9, "Too High"),    # "10" < "9" as strings, but 10 > 9 numerically
        (25, 100, "Too Low"),   # "25" > "100" as strings
        (100, 25, "Too High"),  # "100" < "25" as strings
        (1, 100, "Too Low"),
        (100, 1, "Too High"),
    ],
)
def test_numeric_not_lexicographic_comparison(guess, secret, expected):
    # Regression: comparing as strings gave wrong hints when digit counts differed
    outcome, _ = check_guess(guess, secret)
    assert outcome == expected



---

## 3. Debugging and testing your fixes

- How did you decide whether a bug was really fixed?
I relaunched the game to see if the new changes made were fixed for the small bugs like the difficulty scaling inconsistencies and so forth. For the other, more important bugs like the being given the wrong hints, I used Claude Code to write test cases and run them. I verified the logic of these test cases that they matched the expected behavior afterward.
- Describe at least one test you ran (manual or using pytest)  
  and what it showed you about your code.

  I ran that an undershot guess (say secret is 10 and guess was 5) led to an output of something like "Too Low, Guess Higher" and vice versa. This test passed. I also checked the opposite and made sure that it did NOT say "Guess Lower" since the guess was already too low to begin with.
- Did AI help you design or understand any tests? How?

  It helped in designed all the tests, I just manually went over them to verify that the checked for the expected behavior. Moreover, it actually wrote other tests out of scope for the project to verify how Python compares numbers in Strings such as "9" > "10" but I removed those as the code relevant to the test case was removed. For the tests, that were kept, it checked overshot guesses yieled a "Too High, Guess Lower" response and vice versa. Another test case checked that the correct guess yield a "Win" output.

---

## 4. What did you learn about Streamlit and state?

- How would you explain Streamlit "reruns" and session state to a friend who has never used Streamlit? 

From what I could observe. Streamlit runs the current version of the codebase, meaning that it does not dynamically update the code as you write it. I did see the option to rerun the codebase while I was on the website instance and making edits, however i opted to close the running instance and start a new one just out of old habits. It seems to also have session states where winning status can be preserved across other functionilty of the web app. For example, a bug I found was the once a game was won, the state of the game stayed as won despite clicking a button to make a new game. Once I fixed this to reflect that a clean state after clicking a new game, I realized that states can be preserved across the app while interacting with other features. Even though, this was an issue in this instance, it may be helpful in other projects. If I were explaining to a friend, I would describe it using a Spongebob analogy. Say that Squidward tells Spongebob an order, Spongebob can make it, cook it, etc. However, the order needs to be changed for whatever reason. Spongebob can clean the grill and start making the order again with the changes made. In terms of session state. Lets say spongebob completed an order, he can multitask and start gathering ingredients for another patty or doing something else, and it does not affect the fact that his previous order is still cooked and ready to go.

---

## 5. Looking ahead: your developer habits

- What is one habit or strategy from this project that you want to reuse in future labs or projects?
  - This could be a testing habit, a prompting strategy, or a way you used Git.

  I want to start using the multi-task in one prompt approach again in future projects. I liked how I could prompt Claude Code to do multiple things in one go instead of specifying one by one. This made making changes much easier. However, I think this is something I have to be cautious about because it can introduce more complexity in the responses.
- What is one thing you would do differently next time you work with AI on a coding task?
  One thing I would do differently is be more intentional about the changes I want and be sure I want those changes. With the multi-task single prompts, it kind of got confusing to me when agent asked to do other things and suggested more changes than I wanted. It made the process of reviewing the changes more tedious and tiring. So, instead of writing those multi-task prompt willy-nilly, I need to ensure I understand the entire context of what I want to do and want to change so that any suggestions and push back from an agent can be met with proper context. In other words, think of it like showing up prepared to debate another lawyer.
- In one or two sentences, describe how this project changed the way you think about AI generated code.

It definitely made me more impressed to what agents can do now. Before Claude Code I would just use conversational prompts, but with the full context of projects, Claude Code seems much more powerful and much less likely to suggest over-engineered code that checks for every little possible type of input. On the flip side however, I made me more catious of it because now I treat it with a little bit more respect. Now I have to really debate with it to see if I agree with changes it suggests now that it has a majority if not all the context of the problem/project I am trying to solve.

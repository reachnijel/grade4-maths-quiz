"""Generate questions.js: 100 Class 4 maths multiple-choice questions.

Answers are computed in Python wherever possible, and every question is validated
(4 distinct options, answer present) before the file is written.

    python tools/build_questions.py
"""

from __future__ import annotations

import json
import random
from fractions import Fraction as Fr
from pathlib import Path

OUT = Path(__file__).resolve().parents[1] / "questions.js"
Q: list[dict] = []


def n(x: int) -> str:
    return f"{x:,}"


def add(topic: str, text: str, answer, wrong: list, explain: str) -> None:
    """wrong items are either a value or (value, why-this-is-a-common-mistake)."""
    opts = [str(answer)]
    why: dict[str, str] = {}
    for w in wrong:
        val, reason = (w if isinstance(w, tuple) else (w, None))
        val = str(val)
        assert val not in opts, f"duplicate option {val!r} in: {text}"
        opts.append(val)
        if reason:
            why[val] = reason
    assert len(opts) == 4, f"need 4 options: {text}"
    Q.append({"topic": topic, "q": text, "options": opts, "explain": explain, "why": why})


# ---------------------------------------------------------------- Numbers & Place Value
T = "Numbers & Place Value"
add(T, "What is the place value of 7 in 47,325?", "7,000",
    [("700", "700 would mean 7 is in the hundreds place, but 3 is there."), "70,000",
     ("7", "7 is the face value (the digit itself), not the place value.")],
    "47,325 = 4 ten-thousands + 7 thousands + 3 hundreds + 2 tens + 5 ones. The 7 is in the thousands place, "
    "so its value is 7 × 1,000 = 7,000.")
add(T, "Write 'thirty-four thousand five hundred six' in numerals.", "34,506",
    [("34,560", "That is five hundred sixty, not five hundred six."), "3,456", "34,056"],
    "Thirty-four thousand → 34,000. Five hundred six → 506. 34,000 + 506 = 34,506. "
    "There are no tens, so the tens place is 0.")
add(T, "Which is the expanded form of 60,409?", "60,000 + 400 + 9",
    ["6,000 + 400 + 9", ("60,000 + 40 + 9", "4 is in the hundreds place, so it means 400, not 40."), "600 + 40 + 9"],
    "60,409 has 6 ten-thousands (60,000), 0 thousands, 4 hundreds (400), 0 tens and 9 ones. "
    "So 60,409 = 60,000 + 400 + 9.")
add(T, "Which number is the greatest?", "45,762", ["45,672", "45,267", "45,627"],
    "All numbers start with 45, so compare the hundreds digit: 7 is the biggest. 45,762 is the greatest.")
add(T, "What is the smallest 5-digit number?", n(10000),
    ["99,999", "11,111", ("9,999", "9,999 has only 4 digits; it is the largest 4-digit number.")],
    "The smallest 5-digit number has 1 in front and 0 everywhere else: 10,000. "
    "It is 1 more than the largest 4-digit number 9,999.")
add(T, "Using each of the digits 3, 0, 7, 1, 5 once, what is the smallest 5-digit number?", "10,357",
    ["13,057", "75,310", "10,375"],
    "A number cannot start with 0, so start with the smallest non-zero digit, 1. Then write the rest in "
    "increasing order: 0, 3, 5, 7. Answer: 10,357.")
add(T, "What is the successor of 39,999?", n(39999 + 1),
    [("39,998", "39,998 is the predecessor (the number just before)."), "40,001", "49,999"],
    "The successor is the number just after: 39,999 + 1 = 40,000.")
add(T, "What is the predecessor of 50,000?", n(50000 - 1),
    [("50,001", "50,001 is the successor (the number just after)."), "49,000", "40,999"],
    "The predecessor is the number just before: 50,000 − 1 = 49,999.")
add(T, "Round 4,368 to the nearest hundred.", "4,400",
    [("4,300", "The tens digit is 6 (5 or more), so we round up, not down."), "4,000", "4,370"],
    "Look at the tens digit: 6. Since 6 is 5 or more, round the hundreds up: 4,368 → 4,400.")
add(T, "Round 7,250 to the nearest thousand.", "7,000",
    [("8,000", "The hundreds digit is 2 (less than 5), so we round down."), "7,300", "7,200"],
    "Look at the hundreds digit: 2. Since 2 is less than 5, keep the thousands the same: 7,250 → 7,000.")
add(T, "How do we write 8,015 in words?", "Eight thousand fifteen",
    ["Eight thousand one hundred fifty", "Eighty thousand fifteen", "Eight hundred fifteen"],
    "8,015 = 8 thousands + 0 hundreds + 1 ten + 5 ones = eight thousand fifteen.")
add(T, "What number does the Roman numeral XIV stand for?", 10 + 4,
    [(16, "That would be XVI (V before I means add)."), 15, 41],
    "X = 10 and IV = 4 (I before V means 5 − 1). So XIV = 10 + 4 = 14.")
add(T, "Which Roman numeral shows 29?", "XXIX",
    [("XXVIIII", "We never write the same symbol 4 times; 9 is written IX."), "XIXX", "XXXI"],
    "29 = 20 + 9. 20 = XX and 9 = IX (10 − 1). So 29 = XXIX.")
add(T, "Which of these numbers is odd?", "3,457", ["2,468", "5,790", "1,234"],
    "A number is odd if its ones digit is 1, 3, 5, 7 or 9. 3,457 ends in 7, so it is odd. "
    "The others end in 8, 0 and 4, which are even.")

# ---------------------------------------------------------------- Addition
T = "Addition"
add(T, "3,456 + 2,378 = ?", n(3456 + 2378),
    [("5,724", "This happens when you forget to carry over the 1s."), "5,844", "5,934"],
    "Ones: 6 + 8 = 14, write 4 carry 1. Tens: 5 + 7 + 1 = 13, write 3 carry 1. "
    "Hundreds: 4 + 3 + 1 = 8. Thousands: 3 + 2 = 5. Answer: 5,834.")
add(T, "24,567 + 13,289 = ?", n(24567 + 13289), ["37,846", "36,856", "37,756"],
    "Add in parts: 24,567 + 13,000 = 37,567. Then 37,567 + 289 = 37,856.")
add(T, "999 + 1 = ?", n(999 + 1), ["9,910", "10,000", "1,001"],
    "999 is the largest 3-digit number. Adding 1 gives the smallest 4-digit number: 1,000.")
add(T, "A school has 1,245 boys and 1,378 girls. How many children are there in all?", n(1245 + 1378),
    ["2,523", ("133", "133 is the difference. 'In all' means add."), "2,613"],
    "'In all' means add: 1,245 + 1,378 = 2,623 children.")
add(T, "4,508 + 3,492 = ?", n(4508 + 3492), ["7,990", "8,100", "7,000"],
    "Notice 508 + 492 = 1,000. So 4,000 + 3,000 + 1,000 = 8,000.")
add(T, "Estimate 398 + 512 by rounding each number to the nearest hundred.", 400 + 500,
    [800, 1000, ("910", "910 is the exact answer, not the estimate.")],
    "398 rounds to 400 and 512 rounds to 500. Estimate: 400 + 500 = 900. (Exact answer is 910, close to 900.)")
add(T, "2,750 + ___ = 5,000. What is the missing number?", n(5000 - 2750),
    ["2,350", ("7,750", "That is 2,750 + 5,000. We need the number that, added to 2,750, makes 5,000."), "3,250"],
    "Missing number = 5,000 − 2,750 = 2,250. Check: 2,750 + 2,250 = 5,000.")
add(T, "A shop sold 1,260 kg of rice on Monday and 985 kg on Tuesday. How much rice was sold in the two days?",
    f"{n(1260 + 985)} kg", ["2,145 kg", "275 kg", "2,235 kg"],
    "Total = 1,260 + 985 = 2,245 kg.")

# ---------------------------------------------------------------- Subtraction
T = "Subtraction"
add(T, "5,000 − 1,236 = ?", n(5000 - 1236),
    [("4,236", "This happens when you subtract the smaller digit from the bigger one in each column "
               "instead of borrowing."), "3,774", "6,236"],
    "Trick: 5,000 − 1,236 is 1 more than 4,999 − 1,236 = 3,763. So the answer is 3,764. "
    "Check: 1,236 + 3,764 = 5,000.")
add(T, "8,402 − 3,567 = ?", n(8402 - 3567),
    [("5,165", "This happens when you take the smaller digit from the bigger one instead of borrowing."),
     "4,935", "4,845"],
    "Borrow where needed: 8,402 − 3,567 = 4,835. Check by adding: 3,567 + 4,835 = 8,402.")
add(T, "70,000 − 25,486 = ?", n(70000 - 25486), ["45,514", "44,614", "54,514"],
    "70,000 − 25,000 = 45,000. Then 45,000 − 486 = 44,514.")
add(T, "2,500 tickets were printed and 1,875 were sold. How many tickets are left?", n(2500 - 1875),
    ["725", ("4,375", "'Left' means subtract, not add."), "635"],
    "Tickets left = 2,500 − 1,875 = 625.")
add(T, "___ − 1,250 = 3,750. What is the missing number?", n(3750 + 1250),
    [("2,500", "That is 3,750 − 1,250. The missing number is the biggest one, so add."), "4,000", "5,250"],
    "If something minus 1,250 leaves 3,750, then the number is 3,750 + 1,250 = 5,000.")
add(T, "What is the difference between the largest 4-digit number and the smallest 4-digit number?",
    n(9999 - 1000), ["9,000", "8,000", "9,998"],
    "Largest 4-digit number = 9,999. Smallest 4-digit number = 1,000. 9,999 − 1,000 = 8,999.")
add(T, "How much more is 6,100 than 4,850?", n(6100 - 4850),
    ["2,250", "1,350", ("10,950", "'How much more' asks for the difference, so subtract.")],
    "Difference = 6,100 − 4,850 = 1,250.")
add(T, "A train had 1,130 passengers. At a station 465 got off and 290 got on. How many are on the train now?",
    n(1130 - 465 + 290),
    [("375", "People who got ON must be added, not subtracted."), "1,885", "965"],
    "Got off → subtract: 1,130 − 465 = 665. Got on → add: 665 + 290 = 955 passengers.")

# ---------------------------------------------------------------- Multiplication
T = "Multiplication"
add(T, "23 × 4 = ?", 23 * 4, [("82", "Remember to carry: 3 × 4 = 12, write 2 carry 1."), 27, 812],
    "3 × 4 = 12: write 2, carry 1. 2 × 4 = 8, plus 1 = 9. Answer: 92. (Or 20 × 4 + 3 × 4 = 80 + 12 = 92.)")
add(T, "125 × 8 = ?", n(125 * 8), ["900", "1,250", "1,100"],
    "125 × 8 = 100 × 8 + 25 × 8 = 800 + 200 = 1,000.")
add(T, "46 × 25 = ?", n(46 * 25), ["1,050", "1,250", "322"],
    "46 × 20 = 920 and 46 × 5 = 230. 920 + 230 = 1,150.")
add(T, "312 × 3 = ?", 312 * 3, [836, 963, 315],
    "300 × 3 = 900, 10 × 3 = 30, 2 × 3 = 6. 900 + 30 + 6 = 936.")
add(T, "9 × 12 = ?", 9 * 12, [98, 118, 21],
    "9 × 12 = 9 × 10 + 9 × 2 = 90 + 18 = 108.")
add(T, "36 × 100 = ?", n(36 * 100),
    [("360", "Multiplying by 100 adds two zeros, not one."), "36,000", "136"],
    "To multiply by 100, write two zeros after the number: 36 × 100 = 3,600.")
add(T, "There are 24 boxes with 12 pencils in each box. How many pencils are there?", 24 * 12,
    [("36", "That is 24 + 12. Equal groups means multiply."), 248, 278],
    "24 × 12 = 24 × 10 + 24 × 2 = 240 + 48 = 288 pencils.")
add(T, "0 × 4,567 = ?", 0 * 4567, ["4,567", "1", "45,670"],
    "Any number multiplied by 0 is 0. (Zero groups of anything is nothing.)")
add(T, "15 × 15 = ?", 15 * 15, [215, ("30", "That is 15 + 15."), 250],
    "15 × 15 = 15 × 10 + 15 × 5 = 150 + 75 = 225.")
add(T, "203 × 6 = ?", n(203 * 6),
    [("128", "The 0 in 203 holds the tens place; don't drop it."), "1,208", "1,818"],
    "203 × 6 = 200 × 6 + 3 × 6 = 1,200 + 18 = 1,218.")

# ---------------------------------------------------------------- Division
T = "Division"
add(T, "84 ÷ 4 = ?", 84 // 4, [12, 22, 20],
    "8 tens ÷ 4 = 2 tens, 4 ones ÷ 4 = 1 one. So 84 ÷ 4 = 21. Check: 21 × 4 = 84.")
add(T, "96 ÷ 8 = ?", 96 // 8, [11, 13, 14], "8 × 12 = 96, so 96 ÷ 8 = 12.")
add(T, "144 ÷ 12 = ?", 144 // 12, [14, 11, 13], "12 × 12 = 144, so 144 ÷ 12 = 12.")
add(T, "125 ÷ 5 = ?", 125 // 5, [20, 30, 24], "5 × 25 = 125, so 125 ÷ 5 = 25.")
assert divmod(50, 7) == (7, 1)
add(T, "What are the quotient and remainder when 50 is divided by 7?", "7 remainder 1",
    [("6 remainder 8", "The remainder must always be smaller than the divisor (7)."), "8 remainder 1",
     "7 remainder 0"],
    "7 × 7 = 49, which is the biggest multiple of 7 not more than 50. 50 − 49 = 1. "
    "So quotient = 7, remainder = 1.")
add(T, "0 ÷ 5 = ?", 0, [5, 1, "Cannot be done"],
    "Zero shared among 5 people gives each person 0. So 0 ÷ 5 = 0. (But we can never divide BY 0.)")
add(T, "72 sweets are shared equally among 9 children. How many does each child get?", 72 // 9,
    [7, 9, ("81", "That is 72 + 9. Sharing equally means divide.")],
    "72 ÷ 9 = 8, because 9 × 8 = 72. Each child gets 8 sweets.")
add(T, "365 ÷ 5 = ?", 365 // 5, [63, 71, 75],
    "350 ÷ 5 = 70 and 15 ÷ 5 = 3. 70 + 3 = 73. Check: 73 × 5 = 365.")
assert 91 % 7 == 0 and 92 % 7 and 85 % 4 and 50 % 3
add(T, "Which division leaves NO remainder?", "91 ÷ 7", ["92 ÷ 7", "85 ÷ 4", "50 ÷ 3"],
    "7 × 13 = 91, so 91 ÷ 7 = 13 exactly. The others leave remainders: 92 ÷ 7 = 13 r 1, "
    "85 ÷ 4 = 21 r 1, 50 ÷ 3 = 16 r 2.")

# ---------------------------------------------------------------- Factors & Multiples
T = "Factors & Multiples"
f12 = [d for d in range(1, 13) if 12 % d == 0]
add(T, "How many factors does 12 have?", len(f12), [4, 5, 12],
    f"The factors of 12 are {', '.join(map(str, f12))}. That is {len(f12)} factors. "
    "Don't forget 1 and 12 itself!")
add(T, "Which of these is a multiple of 7?", 63, [53, 74, 27],
    "7 × 9 = 63, so 63 is a multiple of 7. 53, 74 and 27 are not in the 7 times table.")
add(T, "What is the biggest number that divides both 18 and 24 exactly?", 6,
    [3, 2, ("12", "12 does not divide 18 exactly.")],
    "Factors of 18: 1, 2, 3, 6, 9, 18. Factors of 24: 1, 2, 3, 4, 6, 8, 12, 24. "
    "Common factors: 1, 2, 3, 6. The biggest is 6.")
add(T, "What is the smallest number that is a multiple of both 4 and 6?", 12,
    [("24", "24 is a common multiple, but not the smallest one."), 10, 2],
    "Multiples of 4: 4, 8, 12, 16 … Multiples of 6: 6, 12, 18 … The first one in both lists is 12.")
add(T, "Which of these is a prime number?", 13, [9, 15, 21],
    "A prime number has exactly two factors: 1 and itself. 13 is prime. "
    "9 = 3 × 3, 15 = 3 × 5, 21 = 3 × 7 are not prime.")
assert 36 % 8
add(T, "Which number is NOT a factor of 36?", 8, [4, 9, 12],
    "36 ÷ 8 = 4 remainder 4, so 8 is not a factor. 4 × 9 = 36 and 12 × 3 = 36, so 4, 9 and 12 are factors.")

# ---------------------------------------------------------------- Fractions
T = "Fractions"
add(T, "A cake is cut into 8 equal pieces and 3 pieces are eaten. What fraction of the cake is eaten?", "3/8",
    [("5/8", "5/8 is the part that is LEFT, not eaten."), "3/5", "8/3"],
    "The cake has 8 equal parts (denominator 8). 3 parts are eaten (numerator 3). So 3/8 is eaten.")
assert Fr(4, 8) == Fr(1, 2)
add(T, "Which fraction is equal to 1/2?", "4/8", ["2/3", "3/5", "1/4"],
    "4/8: 4 is exactly half of 8, so 4/8 = 1/2. (Divide top and bottom by 4.)")
assert Fr(3, 4) > Fr(2, 3)
add(T, "Which is greater: 3/4 or 2/3?", "3/4", ["2/3", "Both are equal", "Cannot be compared"],
    "Make the denominators the same: 3/4 = 9/12 and 2/3 = 8/12. 9/12 is more, so 3/4 is greater.")
add(T, "What is 1/4 of 20?", 20 // 4, [4, ("15", "15 is 3/4 of 20."), 80],
    "1/4 of 20 means divide 20 into 4 equal parts: 20 ÷ 4 = 5.")
assert Fr(2, 5) + Fr(1, 5) == Fr(3, 5)
add(T, "2/5 + 1/5 = ?", "3/5", [("3/10", "When the denominators are the same, add only the numerators."),
                               "2/25", "1/5"],
    "Same denominator, so add the numerators: 2 + 1 = 3. Keep the denominator 5. Answer: 3/5.")
assert Fr(7, 9) - Fr(4, 9) == Fr(1, 3)
add(T, "7/9 − 4/9 = ? (in simplest form)", "1/3", ["3/18", "11/9", "4/9"],
    "Subtract the numerators: 7 − 4 = 3, so we get 3/9. Divide top and bottom by 3: 3/9 = 1/3.")
assert Fr(2, 3) == Fr(8, 12)
add(T, "2/3 = ?/12. What is the missing number?", 8, [6, 4, 9],
    "3 × 4 = 12, so multiply the top by 4 too: 2 × 4 = 8. So 2/3 = 8/12.")
assert Fr(6, 8) == Fr(3, 4)
add(T, "What is 6/8 in its simplest form?", "3/4", ["1/2", "2/3", "3/8"],
    "Both 6 and 8 can be divided by 2: 6 ÷ 2 = 3 and 8 ÷ 2 = 4. So 6/8 = 3/4.")
add(T, "What is 3/4 of 100?", 3 * 100 // 4, [("25", "25 is 1/4 of 100. We need 3 of those quarters."), 34, 70],
    "1/4 of 100 = 25. So 3/4 of 100 = 3 × 25 = 75.")
add(T, "15 minutes is what fraction of an hour?", "1/4", ["1/2", "1/15", "3/4"],
    "1 hour = 60 minutes. 15/60 = 1/4 (because 15 × 4 = 60). So 15 minutes is a quarter of an hour.")
add(T, "Which fraction is the smallest?", "1/8",
    [("1/2", "With unit fractions, a BIGGER denominator means SMALLER pieces."), "1/3", "1/5"],
    "All have numerator 1. The more parts a whole is cut into, the smaller each part. "
    "8 parts are the smallest, so 1/8 is the smallest.")

# ---------------------------------------------------------------- Decimals & Money
T = "Decimals & Money"
add(T, "Write 7/10 as a decimal.", "0.7", ["7.10", ("0.07", "0.07 is 7/100 (seven hundredths)."), "7.0"],
    "7/10 means 7 tenths. The first place after the decimal point is tenths, so 7/10 = 0.7.")
add(T, "Write 1/2 as a decimal.", "0.5", ["1.2", "0.2", "0.12"],
    "1/2 = 5/10 (multiply top and bottom by 5). 5 tenths = 0.5.")
add(T, "Which decimal is the greatest?", "3.4",
    [("3.04", "3.04 has 0 tenths; 3.4 has 4 tenths, so 3.4 is bigger."), "3.14", "0.34"],
    "Compare the whole number first (3), then tenths: 3.4 has 4 tenths, 3.14 has 1, 3.04 has 0. So 3.4 is greatest.")
assert 1250 + 775 == 2025
add(T, "₹12.50 + ₹7.75 = ?", "₹20.25", ["₹19.25", "₹20.35", "₹21.25"],
    "Rupees: 12 + 7 = 19. Paise: 50 + 75 = 125 paise = ₹1.25. Total: ₹19 + ₹1.25 = ₹20.25.")
add(T, "₹500 − ₹237 = ?", f"₹{500 - 237}", ["₹363", "₹273", "₹337"],
    "₹500 − ₹200 = ₹300, then ₹300 − ₹37 = ₹263.")
add(T, "One pen costs ₹15. How much do 4 pens cost?", f"₹{15 * 4}",
    [("₹19", "That is ₹15 + ₹4. For 4 pens, multiply."), "₹45", "₹65"],
    "4 × ₹15 = ₹60.")
add(T, "How many paise make ₹1?", 100, [10, "1,000", 50], "₹1 = 100 paise. So 50 paise is half a rupee.")
add(T, "You buy a toy for ₹145 and pay with a ₹200 note. How much change do you get?", f"₹{200 - 145}",
    ["₹65", "₹45", ("₹345", "Change means what comes back, so subtract.")],
    "Change = ₹200 − ₹145 = ₹55. (Count up: ₹145 + ₹5 = ₹150, + ₹50 = ₹200 → ₹55.)")

# ---------------------------------------------------------------- Time
T = "Time"
add(T, "How is 3:45 p.m. written in 24-hour time?", "15:45", ["13:45", "03:45", "17:45"],
    "For p.m. times (after noon), add 12 to the hour: 3 + 12 = 15. So 3:45 p.m. = 15:45.")
add(T, "2 hours 30 minutes = how many minutes?", 2 * 60 + 30,
    [("230", "Hours and minutes can't just be written side by side; 1 hour = 60 minutes."), 130, 160],
    "1 hour = 60 minutes, so 2 hours = 120 minutes. 120 + 30 = 150 minutes.")
add(T, "A class starts at 9:15 a.m. and ends at 11:00 a.m. How long is it?", "1 hour 45 minutes",
    ["2 hours 45 minutes", "1 hour 15 minutes", "2 hours 15 minutes"],
    "9:15 → 10:15 is 1 hour. 10:15 → 11:00 is 45 minutes. Total: 1 hour 45 minutes.")
add(T, "How many days does February have in a leap year?", 29, [("28", "28 days is for a normal year."), 30, 31],
    "February has 28 days in a normal year and 29 days in a leap year (every 4 years, like 2024 and 2028).")
add(T, "7 weeks = how many days?", 7 * 7, [42, 56, 14], "1 week = 7 days, so 7 weeks = 7 × 7 = 49 days.")
add(T, "How many days are there in March?", 31, [30, 28, 29],
    "March has 31 days. Knuckle trick: months on a knuckle (Jan, Mar, May, Jul, Aug, Oct, Dec) have 31 days.")
add(T, "300 seconds = how many minutes?", 300 // 60, [3, 30, 50],
    "1 minute = 60 seconds. 300 ÷ 60 = 5 minutes.")
add(T, "The hour hand is just past 4 and the minute hand points to 6. What time is it?", "4:30",
    [("6:20", "The SHORT hand shows the hour and the LONG hand shows the minutes."), "4:06", "6:04"],
    "Hour hand (short) past 4 → 4 o'clock hour. Minute hand on 6 → 6 × 5 = 30 minutes. Time: 4:30.")

# ---------------------------------------------------------------- Measurement
T = "Measurement"
add(T, "1 kilometre = how many metres?", n(1000), ["100", "10,000", "10"], "Kilo means 1,000. So 1 km = 1,000 m.")
add(T, "3 m 25 cm = how many centimetres?", f"{3 * 100 + 25} cm",
    [("3,025 cm", "1 m = 100 cm (not 1,000), so 3 m = 300 cm."), "3,250 cm", "28 cm"],
    "1 m = 100 cm, so 3 m = 300 cm. 300 + 25 = 325 cm.")
add(T, "2 kg 500 g = how many grams?", f"{n(2 * 1000 + 500)} g", ["2,050 g", "250 g", "25,000 g"],
    "1 kg = 1,000 g, so 2 kg = 2,000 g. 2,000 + 500 = 2,500 g.")
add(T, "4,500 mL is the same as:", "4 L 500 mL", ["45 L", "4 L 50 mL", "450 L"],
    "1 L = 1,000 mL. 4,500 mL = 4,000 mL + 500 mL = 4 L 500 mL.")
add(T, "Which is heavier: 1 kg of cotton or 1 kg of iron?", "Both weigh the same",
    [("1 kg of iron", "Iron feels heavier for its size, but 1 kg is 1 kg!"), "1 kg of cotton", "Cannot say"],
    "Both are exactly 1 kg, so they weigh the same. Cotton just takes up much more space.")
add(T, "Which unit is best for measuring the length of a pencil?", "Centimetres",
    ["Kilometres", ("Kilograms", "Kilograms measure weight, not length."), "Litres"],
    "A pencil is short, about 15–20 cm, so centimetres are best. Kilometres are for long distances.")
add(T, "A bucket holds 10 litres. How many 500 mL mugs of water will fill it?", 10 * 1000 // 500, [5, 50, 2],
    "10 L = 10,000 mL. 10,000 ÷ 500 = 20 mugs. (Or: 2 mugs make 1 L, so 10 L needs 20 mugs.)")

# ---------------------------------------------------------------- Geometry
T = "Geometry"
add(T, "How many sides does a hexagon have?", 6, [5, 7, 8],
    "Hexa means six. A hexagon has 6 sides (like a honeycomb cell). Pentagon = 5, octagon = 8.")
add(T, "What is the perimeter of a rectangle 8 cm long and 5 cm wide?", f"{2 * (8 + 5)} cm",
    [("13 cm", "That adds only one length and one width. A rectangle has 4 sides."),
     ("40 cm", "40 sq cm would be the AREA (8 × 5). Perimeter is the distance around."), "21 cm"],
    "Perimeter = 8 + 5 + 8 + 5 = 26 cm, or 2 × (8 + 5) = 26 cm.")
add(T, "What is the area of a rectangle 6 cm long and 4 cm wide?", f"{6 * 4} sq cm",
    [("20 sq cm", "20 cm is the PERIMETER. Area = length × width."), "10 sq cm", "48 sq cm"],
    "Area = length × width = 6 × 4 = 24 square centimetres.")
add(T, "How many degrees are there in a right angle?", "90°", ["45°", "180°", "60°"],
    "A right angle is a square corner, like the corner of a book. It measures 90°. A straight line is 180°.")
add(T, "How many corners (vertices) does a cube have?", 8,
    [("6", "6 is the number of FACES of a cube."), ("12", "12 is the number of EDGES of a cube."), 4],
    "A cube has 8 corners: 4 on the top and 4 on the bottom. It also has 6 faces and 12 edges.")
add(T, "A circle has a radius of 5 cm. What is its diameter?", f"{2 * 5} cm", ["2.5 cm", "25 cm", "15 cm"],
    "Diameter = 2 × radius = 2 × 5 = 10 cm. The diameter goes all the way across through the centre.")
add(T, "How many lines of symmetry does a square have?", 4,
    [("2", "Don't forget the two diagonal lines!"), 1, 8],
    "A square can be folded in half 4 ways: 1 across, 1 up-down and 2 along the diagonals.")

# ---------------------------------------------------------------- Patterns & Data
T = "Patterns & Data"
add(T, "What comes next? 5, 10, 20, 40, ___", 40 * 2, [45, 50, 60],
    "Each number is double the one before: 5 × 2 = 10, 10 × 2 = 20, 20 × 2 = 40, so next is 40 × 2 = 80.")
add(T, "What comes next? 100, 91, 82, 73, ___", 73 - 9, [63, 65, 72],
    "Each number is 9 less than the one before. 73 − 9 = 64.")
add(T, "In a pictograph, 1 picture = 5 books. Ravi's row has 7 pictures. How many books did Ravi read?", 7 * 5,
    [12, ("7", "Each picture stands for 5 books, not 1."), 30],
    "7 pictures × 5 books each = 35 books.")
add(T, "Meena made 4 complete tally bundles (each bundle is 5 marks) and 2 more single marks. What number is that?",
    4 * 5 + 2, [6, 42, 20],
    "Each bundle shows 5. 4 bundles = 4 × 5 = 20. Add the 2 single marks: 20 + 2 = 22.")


# ---------------------------------------------------------------- shuffle + validate + write
def build() -> list[dict]:
    out = []
    for i, q in enumerate(Q, 1):
        opts = q["options"][:]
        correct = opts[0]
        random.Random(1000 + i).shuffle(opts)
        out.append({"id": i, "topic": q["topic"], "q": q["q"], "options": opts,
                    "answer": opts.index(correct), "explain": q["explain"], "why": q["why"]})
    assert len(out) == 100, f"expected 100 questions, got {len(out)}"
    assert len({q["q"] for q in out}) == 100, "duplicate question text"
    for q in out:
        assert len(set(q["options"])) == 4 and 0 <= q["answer"] < 4
        assert all(k in q["options"] and k != q["options"][q["answer"]] for k in q["why"])
    return out


if __name__ == "__main__":
    data = build()
    OUT.write_text("// Generated by tools/build_questions.py - edit that file, not this one.\n"
                   "window.QUESTIONS = " + json.dumps(data, ensure_ascii=False, indent=1) + ";\n", encoding="utf-8")
    pos = [q["answer"] for q in data]
    print(f"wrote {len(data)} questions to {OUT.name}; answer positions A-D: {[pos.count(i) for i in range(4)]}")

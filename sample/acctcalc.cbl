       IDENTIFICATION DIVISION.
       PROGRAM-ID. ACCTCALC.
       DATA DIVISION.
       WORKING-STORAGE SECTION.
       01 WS-BALANCE   PIC 9(7)V99.
       01 WS-RATE      PIC 9V999.
       01 WS-INTEREST  PIC 9(7)V99.
       01 WS-FEE       PIC 9(3)V99.
       01 WS-AGE       PIC 99.
       01 WS-INCOME    PIC 9(7).
       01 WS-ELIGIBLE  PIC X.
       PROCEDURE DIVISION.
       MAIN-PARA.
           PERFORM CALC-INTEREST.
           PERFORM CALC-FEE.
           PERFORM CHECK-LOAN.
           STOP RUN.
       CALC-INTEREST.
      * Savings interest tiers
           EVALUATE TRUE
               WHEN WS-BALANCE > 100000
                   MOVE 0.045 TO WS-RATE
               WHEN WS-BALANCE > 10000
                   MOVE 0.030 TO WS-RATE
               WHEN OTHER
                   MOVE 0.015 TO WS-RATE
           END-EVALUATE.
           COMPUTE WS-INTEREST = WS-BALANCE * WS-RATE / 12.
       CALC-FEE.
           IF WS-BALANCE < 1000
               MOVE 12.50 TO WS-FEE
           ELSE
               MOVE 0 TO WS-FEE
           END-IF.
       CHECK-LOAN.
           IF WS-AGE >= 18 AND WS-INCOME > 25000
               MOVE 'Y' TO WS-ELIGIBLE
           END-IF.

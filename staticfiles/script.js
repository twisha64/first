console.log("Board data:", board);

const sudoku = document.getElementById("sudoku");

let seconds = 0;
let timerInterval = null;
let selectedCell = null;

/* ================= TIMER ================= */

function startTimer() {
    stopTimer();

    timerInterval = setInterval(() => {
        seconds++;

        let mins = Math.floor(seconds / 60);
        let secs = seconds % 60;

        document.getElementById("timer").innerText =
            `Time: ${String(mins).padStart(2, "0")}:${String(secs).padStart(2, "0")}`;
    }, 1000);
}

function stopTimer() {
    if (timerInterval) clearInterval(timerInterval);
    timerInterval = null;
}

function resetTimer() {
    stopTimer();
    seconds = 0;
    document.getElementById("timer").innerText = "Time: 00:00";
}

/* ================= DRAW BOARD ================= */

function drawBoard() {
    sudoku.innerHTML = "";

    board.forEach((row, r) => {
        row.forEach((num, c) => {
            const cell = document.createElement("input");
            cell.type = "text";
            cell.maxLength = 1;
            cell.className = "cell";

            cell.dataset.row = r;
            cell.dataset.col = c;

            if (num !== 0) {
                cell.value = num;
                cell.disabled = true;
                cell.classList.add("fixed");
            }

            cell.addEventListener("input", () => {
                if (!/^[1-9]$/.test(cell.value)) {
                    cell.value = "";
                }
            });

            if (c % 3 === 0) cell.classList.add("left-border");
            if (r % 3 === 0) cell.classList.add("top-border");
            if (c === 8) cell.classList.add("right-border");
            if (r === 8) cell.classList.add("bottom-border");

            sudoku.appendChild(cell);
        });
    });
}

/* ================= GET BOARD ================= */

function getBoard() {
    const inputs = document.querySelectorAll(".cell");
    let data = [];
    let i = 0;

    for (let r = 0; r < 9; r++) {
        let row = [];
        for (let c = 0; c < 9; c++) {
            const v = inputs[i].value;
            row.push(v === "" ? 0 : parseInt(v));
            i++;
        }
        data.push(row);
    }

    return data;
}

/* ================= UPDATE SCORE ================= */

function updateScore(change) {
    fetch("/update_score/", {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
            "X-CSRFToken": getCookie("csrftoken")
        },
        body: JSON.stringify({ change: change })
    })
    .then(res => res.json())
    .then(data => {
        document.getElementById("score").innerText = data.score;
    });
}

/* ================= CHECK SOLUTION ================= */

function checkSolution() {
    fetch("/check/", {
        method: "POST",
        headers: {
            "Content-Type": "application/x-www-form-urlencoded",
            "X-CSRFToken": getCookie("csrftoken")
        },
        body: "board=" + JSON.stringify(getBoard())
    })
    .then(res => res.json())
    .then(data => {
        const inputs = document.querySelectorAll(".cell");

        let index = 0;
        let change = 0;
        let allCorrect = true;

        data.result.flat().forEach(status => {
            const cell = inputs[index];

            if (!cell.classList.contains("fixed")) {

                // ✅ only score if not already marked correct
                if (!cell.classList.contains("correct")) {

                    if (status === "correct") {
                        cell.classList.add("correct");
                        change += 5;
                    }

                    if (status === "wrong") {
                        cell.classList.add("wrong");
                        change -= 2;
                        allCorrect = false;
                    }

                    if (status === "empty") {
                        allCorrect = false;
                    }
                }
            }

            index++;
        });

        if (change !== 0) {
            updateScore(change);
        }

        if (allCorrect) {
            stopTimer();

            fetch("/save_score/", {
                method: "POST",
                headers: {
                    "Content-Type": "application/x-www-form-urlencoded",
                    "X-CSRFToken": getCookie("csrftoken")
                },
                body: "time=" + seconds
            });

            alert("🎉 Puzzle Completed!");
        }
    });
}


/* ================= CLEAR BOARD ================= */

function clearBoard() {
    document.querySelectorAll(".cell").forEach(cell => {
        if (!cell.disabled) {
            cell.value = "";
            cell.classList.remove("correct", "wrong");
        }
    });

    resetTimer();
    startTimer();
}

/* ================= CELL SELECT ================= */

document.addEventListener("click", e => {
    if (e.target.classList.contains("cell") && !e.target.disabled) {
        document.querySelectorAll(".cell").forEach(c =>
            c.classList.remove("selected")
        );

        e.target.classList.add("selected");
        selectedCell = e.target;
    }
});

/* ================= HINT ================= */

function useHint() {
    if (!selectedCell) {
        alert("Select a cell first");
        return;
    }

    const row = selectedCell.dataset.row;
    const col = selectedCell.dataset.col;

    fetch("/hint/", {
        method: "POST",
        headers: {
            "Content-Type": "application/x-www-form-urlencoded",
            "X-CSRFToken": getCookie("csrftoken")
        },
        body: `row=${row}&col=${col}`
    })
    .then(res => res.json())
    .then(data => {
        if (data.error) {
            alert(data.error);
            return;
        }

        selectedCell.value = data.value;
        document.getElementById("hint-count").innerText =
            "Hints left: " + data.hints_left;

        updateScore(-10);
    });
}

/* ================= NEW GAME ================= */

function newGame() {
    window.location.reload();
}

/* ================= COOKIE ================= */

function getCookie(name) {
    let value = null;

    document.cookie.split(";").forEach(cookie => {
        cookie = cookie.trim();
        if (cookie.startsWith(name + "=")) {
            value = decodeURIComponent(
                cookie.substring(name.length + 1)
            );
        }
    });

    return value;
}

/* ================= START ================= */

drawBoard();
startTimer();
 function solveSudoku() {
    fetch("/solve/", {
        method: "POST",
        headers: {
            "Content-Type": "application/x-www-form-urlencoded",
            "X-CSRFToken": getCookie("csrftoken")
        },
        body: "board=" + JSON.stringify(getBoard())
    })
    .then(res => res.json())
    .then(data => {
        const inputs = document.querySelectorAll(".cell");
        let index = 0;

        data.solution.flat().forEach(value => {
            inputs[index].value = value;
            inputs[index].classList.add("correct");
            index++;
        });

        alert("Sudoku Solved by AI 🧠");
    });
}

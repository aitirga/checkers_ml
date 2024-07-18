const canvas = document.getElementById('checkersBoard');
const ctx = canvas.getContext('2d');
const statusElement = document.getElementById('status');

const BOARD_SIZE = 8;
const SQUARE_SIZE = canvas.width / BOARD_SIZE;

let board = Array(BOARD_SIZE).fill().map(() => Array(BOARD_SIZE).fill(null));
let selectedPiece = null;
let currentPlayer = 'white';

// function initializeBoard() {
//     for (let row = 0; row < BOARD_SIZE; row++) {
//         for (let col = 0; col < BOARD_SIZE; col++) {
//             if ((row + col) % 2 === 1) {
//                 if (row < 3) board[row][col] = 'red';
//                 else if (row > 4) board[row][col] = 'black';
//             }
//         }
//     }
// }

async function drawBoard() {
    board = await fetch('/api/board').then(response => response.json());
    for (let row = 0; row < BOARD_SIZE; row++) {
        for (let col = 0; col < BOARD_SIZE; col++) {
            ctx.fillStyle = (row + col) % 2 === 0 ? '#E0E0E0' : '#404040';
            ctx.fillRect(col * SQUARE_SIZE, row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE);

            if (board[row][col]) {
                ctx.fillStyle = board[row][col];
                ctx.beginPath();
                ctx.arc(
                    col * SQUARE_SIZE + SQUARE_SIZE / 2,
                    row * SQUARE_SIZE + SQUARE_SIZE / 2,
                    SQUARE_SIZE / 2 - 5,
                    0,
                    2 * Math.PI
                );
                ctx.fill();
            }
        }
    }
}

// canvas.addEventListener('click', async (event) => {
//     const rect = canvas.getBoundingClientRect();
//     const x = event.clientX - rect.left;
//     const y = event.clientY - rect.top;
//     const col = Math.floor(x / SQUARE_SIZE);
//     const row = Math.floor(y / SQUARE_SIZE);
//
//     if (!selectedPiece) {
//         if (board[row][col]) {
//             selectedPiece = { row, col };
//         }
//     } else {
//         const result = await makeMove(selectedPiece.row, selectedPiece.col, row, col);
//         if (result.valid) {
//             board = result.board;
//             statusElement.textContent = result.currentPlayer + "'s turn";
//         }
//         selectedPiece = null;
//     }
//     drawBoard();
// });

// async function makeMove(fromRow, fromCol, toRow, toCol) {
//     const response = await fetch('/api/move', {
//         method: 'POST',
//         headers: {
//             'Content-Type': 'application/json',
//         },
//         body: JSON.stringify({
//             from: { row: fromRow, col: fromCol },
//             to: { row: toRow, col: toCol },
//             board: board
//         }),
//     });
//     return await response.json();
// }

async function initGame() {
    const response = await fetch('/api/reset');
    board = await response.json();
    drawBoard();
}

nextButton.addEventListener('click', async () => {
    try {
        const response = await fetch('/api/next', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ board: board , currentPlayer: currentPlayer }),
        });
        if (!response.ok) {
            throw new Error('Failed to get next move');
        }
        const result = await response.json();

        if (result.valid) {
            board = result.board;
            currentPlayer = result.currentPlayer;
            statusElement.textContent = result.currentPlayer + "'s turn";
            drawBoard();
        } else {
            statusElement.textContent = 'No valid moves available';
        }
    } catch (error) {
        console.error('Error getting next move:', error);
        statusElement.textContent = 'Error getting next move. Please try again.';
    }
});

resetButton.addEventListener('click', initGame);

drawBoard();
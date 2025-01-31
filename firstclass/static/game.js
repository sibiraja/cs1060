class Game2048 {
    constructor() {
        this.grid = Array(4).fill().map(() => Array(4).fill(0));
        this.score = 0;
        this.setupGrid();
        this.addNewTile();
        this.addNewTile();
        this.setupEventListeners();
        this.updateDisplay();
    }

    setupGrid() {
        const gridContainer = document.getElementById('grid');
        for (let i = 0; i < 16; i++) {
            const cell = document.createElement('div');
            cell.className = 'cell';
            gridContainer.appendChild(cell);
        }
    }

    updateDisplay() {
        const cells = document.querySelectorAll('.cell');
        let cellIndex = 0;
        for (let i = 0; i < 4; i++) {
            for (let j = 0; j < 4; j++) {
                const value = this.grid[i][j];
                cells[cellIndex].textContent = value || '';
                cells[cellIndex].setAttribute('data-value', value);
                cellIndex++;
            }
        }
        document.getElementById('score').textContent = this.score;
    }

    addNewTile() {
        const emptyCells = [];
        for (let i = 0; i < 4; i++) {
            for (let j = 0; j < 4; j++) {
                if (this.grid[i][j] === 0) {
                    emptyCells.push({i, j});
                }
            }
        }
        if (emptyCells.length > 0) {
            const {i, j} = emptyCells[Math.floor(Math.random() * emptyCells.length)];
            this.grid[i][j] = Math.random() < 0.9 ? 2 : 4;
        }
    }

    move(direction) {
        let moved = false;
        const oldGrid = JSON.stringify(this.grid);

        switch(direction) {
            case 'ArrowLeft':
                moved = this.moveLeft();
                break;
            case 'ArrowRight':
                this.grid = this.grid.map(row => row.reverse());
                moved = this.moveLeft();
                this.grid = this.grid.map(row => row.reverse());
                break;
            case 'ArrowUp':
                this.grid = this.transpose(this.grid);
                moved = this.moveLeft();
                this.grid = this.transpose(this.grid);
                break;
            case 'ArrowDown':
                this.grid = this.transpose(this.grid);
                this.grid = this.grid.map(row => row.reverse());
                moved = this.moveLeft();
                this.grid = this.grid.map(row => row.reverse());
                this.grid = this.transpose(this.grid);
                break;
        }

        if (moved) {
            this.addNewTile();
            this.updateDisplay();
            if (this.isGameOver()) {
                alert('Game Over! Your score: ' + this.score);
            }
        }
    }

    moveLeft() {
        let moved = false;
        for (let i = 0; i < 4; i++) {
            let row = this.grid[i].filter(cell => cell !== 0);
            for (let j = 0; j < row.length - 1; j++) {
                if (row[j] === row[j + 1]) {
                    row[j] *= 2;
                    this.score += row[j];
                    row.splice(j + 1, 1);
                }
            }
            const newRow = row.concat(Array(4 - row.length).fill(0));
            if (JSON.stringify(this.grid[i]) !== JSON.stringify(newRow)) {
                moved = true;
            }
            this.grid[i] = newRow;
        }
        return moved;
    }

    transpose(grid) {
        return grid[0].map((_, i) => grid.map(row => row[i]));
    }

    isGameOver() {
        // Check for empty cells
        for (let i = 0; i < 4; i++) {
            for (let j = 0; j < 4; j++) {
                if (this.grid[i][j] === 0) return false;
            }
        }

        // Check for possible merges
        for (let i = 0; i < 4; i++) {
            for (let j = 0; j < 3; j++) {
                if (this.grid[i][j] === this.grid[i][j + 1]) return false;
            }
        }
        for (let j = 0; j < 4; j++) {
            for (let i = 0; i < 3; i++) {
                if (this.grid[i][j] === this.grid[i + 1][j]) return false;
            }
        }
        return true;
    }

    setupEventListeners() {
        document.addEventListener('keydown', (event) => {
            if (['ArrowUp', 'ArrowDown', 'ArrowLeft', 'ArrowRight'].includes(event.key)) {
                event.preventDefault();
                this.move(event.key);
            }
        });
    }
}

// Start the game when the page loads
window.addEventListener('load', () => {
    new Game2048();
});

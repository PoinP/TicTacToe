#ifndef BOARD_H

#define BOARD_H

enum class Player
{
	PlayerOne,
	PlayerTwo
};

class Board
{
public:
	Board(char playerOne, char playerTwo);

	void getBestMove(Player player, int& x, int& y);
	void placeMark(Player player, int coordX, int coordY);

	void print() const;
	bool isFull() const;
	bool hasWon(Player player) const;

private:
	const char m_PlayerOne, m_PlayerTwo;
	char m_Board[3][3] = {
		{' ', ' ', ' '},
		{' ', ' ', ' '},
		{' ', ' ', ' '}
	};

	int minimax(Player player, int depth = 0);
};

#endif // !BOARD_H
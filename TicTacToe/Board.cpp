#include "Board.h"

#include <iostream>
#include <algorithm>
#include <stdexcept>

Board::Board(char playerOne, char playerTwo)
    : m_PlayerOne(playerOne), m_PlayerTwo(playerTwo)
{}

void Board::getBestMove(Player player, int& x, int& y)
{
	int maxScore = 1000;
	maxScore *= player == Player::PlayerOne ? -1 : 1;

	char mark;
	Player nextPlayer;

	if (player == Player::PlayerOne)
	{
		mark = m_PlayerOne;
		nextPlayer = Player::PlayerTwo;
	}
	else
	{
		mark = m_PlayerTwo;
		nextPlayer = Player::PlayerOne;
	}

	for (int i = 0; i < 3; i++)
	{
		for (int j = 0; j < 3; j++)
		{
			if (m_Board[i][j] != ' ')
				continue;

			m_Board[i][j] = mark;

			int minimaxResult = minimax(nextPlayer);

			if (player == Player::PlayerOne)
			{
				if (minimaxResult > maxScore)
				{
					x = j;
					y = i;
					maxScore = minimaxResult;
				}
			}
			else
			{
				if (minimaxResult < maxScore)
				{
					x = j;
					y = i;
					maxScore = minimaxResult;
				}
			}

			m_Board[i][j] = ' ';
		}
	}
}

void Board::placeMark(Player player, int coordX, int coordY)
{
	if (coordX < 0 || coordX > 2 || coordY < 0 || coordX > 2)
		throw std::invalid_argument("Invalid coordinates!");

	if (m_Board[coordY][coordX] != ' ')
		throw std::invalid_argument("Space is occupied!");

	char mark = player == Player::PlayerOne ? m_PlayerOne : m_PlayerTwo;

	m_Board[coordY][coordX] = mark;
}

void Board::print() const
{
	std::cout << "-------\n";

	for (int i = 0; i < 3; i++)
	{
		std::cout << "|";
		for (int j = 0; j < 3; j++)
		{
			std::cout << m_Board[i][j] << "|";
		}

		std::cout << "\n-------\n";
	}
}

bool Board::isFull() const
{
	for (int i = 0; i < 3; i++)
	{
		for (int j = 0; j < 3; j++)
		{
			if (m_Board[i][j] == ' ')
				return false;
		}
	}

	return true;
}

bool Board::hasWon(Player player) const
{
	char mark = player == Player::PlayerOne ? m_PlayerOne : m_PlayerTwo;

	// Row Win
	for (int i = 0; i < 3; i++)
	{
		if (m_Board[i][0] == m_Board[i][1] && m_Board[i][1] == m_Board[i][2] && m_Board[i][2] == mark)
			return true;
	}

	// Column Win
	for (int i = 0; i < 3; i++)
	{
		if (m_Board[0][i] == m_Board[1][i] && m_Board[1][i] == m_Board[2][i] && m_Board[2][i] == mark)
			return true;
	}

	// Diagonal Win
	if ((m_Board[0][0] == m_Board[1][1] && m_Board[1][1] == m_Board[2][2] && m_Board[2][2] == mark) ||
		(m_Board[0][2] == m_Board[1][1] && m_Board[1][1] == m_Board[2][0] && m_Board[2][0] == mark))
		return true;

	return false;
}

int Board::minimax(Player player, int depth)
{
	char mark = player == Player::PlayerOne ? m_PlayerOne : m_PlayerTwo;
	bool isMaximizing = player == Player::PlayerOne ? true : false;

	if (hasWon(Player::PlayerOne))
		return 20;

	if (hasWon(Player::PlayerTwo))
		return -20;

	if (isFull())
		return 0;

	if (isMaximizing)
	{
		int bestValue = -1000;

		for (int i = 0; i < 3; i++)
		{
			for (int j = 0; j < 3; j++)
			{
				if (m_Board[i][j] != ' ')
					continue;

				m_Board[i][j] = mark;

				bestValue = std::max(bestValue, minimax(Player::PlayerTwo, ++depth) - depth);

				m_Board[i][j] = ' ';
			}
		}

		return bestValue;
	}
	else
	{
		int bestValue = 1000;

		for (int i = 0; i < 3; i++)
		{
			for (int j = 0; j < 3; j++)
			{
				if (m_Board[i][j] != ' ')
					continue;

				m_Board[i][j] = mark;

				bestValue = std::min(bestValue, minimax(Player::PlayerOne, ++depth) + depth);

				m_Board[i][j] = ' ';
			}
		}

		return bestValue;
	}
}

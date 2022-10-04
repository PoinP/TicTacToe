#include <iostream>

#include "Board.h"

static void playGame();

int main()
{
	playGame();

	return 0;
}

static void playGame()
{
	Board playBoard('X', 'O');

	int pX, pY;
	int aiX, aiY;
	bool isInputValid;

	std::cout << "You are playing with X!" << std::endl;

	while (true)
	{
		playBoard.print();

		if (playBoard.hasWon(Player::PlayerOne))
		{
			std::cout << "Congratulations on beating the AI!" << std::endl;
			break;
		}
		
		if (playBoard.hasWon(Player::PlayerTwo))
		{
			std::cout << "Ahh, you lost to the AI!" << std::endl;
			break;
		}

		isInputValid = false;

		while (!isInputValid)
		{
			std::cout << "Enter coords: ";
			std::cin >> pY >> pX;

			if (!std::cin)
			{
				std::cin.clear();
				std::cin.ignore(1024, '\n');
				continue;
			}

			try
			{
				playBoard.placeMark(Player::PlayerOne, pX, pY);
				isInputValid = true;
			}
			catch (const std::exception& ex)
			{
				std::cout << ex.what() << " Please try again!" << std::endl;
			}
		}

		if (playBoard.isFull())
		{
			playBoard.print();

			std::cout << "You ended the game in a draw!" << std::endl;
			break;
		}

		playBoard.getBestMove(Player::PlayerTwo, aiX, aiY);

		playBoard.placeMark(Player::PlayerTwo, aiX, aiY);
	}
}
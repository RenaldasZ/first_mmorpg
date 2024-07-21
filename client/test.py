import unittest
from unittest.mock import Mock, patch
from src.entities.enemy import Enemy
import time

class TestEnemy(unittest.TestCase):

    def setUp(self) -> None:
        """Set up the test environment with a mock game and player, and initialize an enemy instance."""
        self.game = Mock()
        self.player = Mock()
        self.player._x = 50
        self.player._y = 50
        self.enemy = Enemy(x=0, y=0, game=self.game, level=1, size=100, speed=2, max_health=100, attack_range=50)

    def test_initialization(self) -> None:
        """Test that the enemy initializes with the correct attributes."""
        enemy = self.enemy
        self.assertEqual(enemy.x, 0)
        self.assertEqual(enemy.y, 0)
        self.assertEqual(enemy.level, 1)
        self.assertEqual(enemy.size, 100)
        self.assertEqual(enemy.speed, 2)
        self.assertEqual(enemy.max_health, 100)
        self.assertEqual(enemy.health, 100)
        self.assertTrue(enemy.alive)
        self.assertGreaterEqual(enemy.attack_cooldown, enemy.MIN_COOLDOWN)
        self.assertLessEqual(enemy.attack_cooldown, enemy.MAX_COOLDOWN)
        self.assertGreaterEqual(enemy.respawn_time, enemy.MIN_RESPAWN_TIME)
        self.assertLessEqual(enemy.respawn_time, enemy.MAX_RESPAWN_TIME)

    def test_movement_towards_player(self) -> None:
        """Test that the enemy moves towards the player."""
        initial_x = self.enemy.x
        initial_y = self.enemy.y
        self.enemy._move_towards(self.player._x, self.player._y)
        self.assertNotEqual(self.enemy.x, initial_x)
        self.assertNotEqual(self.enemy.y, initial_y)

    def test_health_percentage(self) -> None:
        """Test the calculation of health percentage after taking damage."""
        self.enemy.take_damage(50)
        self.assertEqual(self.enemy.get_health_percentage(), 50)
        self.enemy.take_damage(25)
        self.assertEqual(self.enemy.get_health_percentage(), 25)

    def test_take_damage_and_destroy(self) -> None:
        """Test the enemy's response to taking lethal damage and being destroyed."""
        self.enemy.take_damage(100)
        self.assertFalse(self.enemy.alive)
        self.assertEqual(self.enemy.health, 0)

    @patch('time.time', return_value=1000)
    def test_attack_player(self, mock_time) -> None:
        """Test the enemy's attack on the player, ensuring cooldown is respected."""
        self.player.take_damage = Mock()
        self.enemy.last_attack_time = 990
        self.enemy.attack_cooldown = 5  # Ensure cooldown period is over
        self.enemy._x = self.player._x
        self.enemy._y = self.player._y

        self.enemy.attack_player(self.player)
        self.player.take_damage.assert_called()

    def test_respawn(self) -> None:
        """Test the respawn behavior of the enemy after being destroyed."""
        self.enemy.destroy()
        self.assertFalse(self.enemy.alive)
        self.enemy.respawn()
        self.assertTrue(self.enemy.alive)
        self.assertEqual(self.enemy.x, self.enemy.initial_x)
        self.assertEqual(self.enemy.y, self.enemy.initial_y)
        self.assertEqual(self.enemy.health, self.enemy.max_health)

    def test_attack_outside_cooldown(self) -> None:
        """Test that the enemy cannot attack the player if the cooldown period has not passed."""
        self.player.take_damage = Mock()
        self.enemy.last_attack_time = time.time()
        self.enemy.attack_player(self.player)
        self.player.take_damage.assert_not_called()

    def test_attack_out_of_range(self) -> None:
        """Test that the enemy cannot attack the player if out of range."""
        self.player.take_damage = Mock()
        self.enemy._x = self.player._x + 1000  # Place enemy far out of range
        self.enemy._y = self.player._y + 1000
        self.enemy.attack_player(self.player)
        self.player.take_damage.assert_not_called()

    def test_respawn_timer(self) -> None:
        """Test that the enemy respawns after the respawn timer."""
        self.enemy.destroy()
        self.assertFalse(self.enemy.alive)
        respawn_time = self.enemy.respawn_time
        self.enemy.respawn_timer = time.time() - 1  # Simulate time passed beyond respawn time
        self.enemy.update(self.player)
        self.assertTrue(self.enemy.alive)

    def test_no_respawn_before_timer(self) -> None:
        """Test that the enemy does not respawn before the respawn timer."""
        self.enemy.destroy()
        self.assertFalse(self.enemy.alive)
        self.enemy.update(self.player)
        self.assertFalse(self.enemy.alive)  # Should still be false since timer not passed

    def test_calculate_distance(self) -> None:
        """Test the distance calculation between enemy and a target point."""
        self.assertEqual(self.enemy._calculate_distance(0, 0), 0)
        self.assertEqual(self.enemy._calculate_distance(3, 4), 5)  # 3-4-5 triangle

    def test_is_within_range(self) -> None:
        """Test if the enemy correctly determines whether a target is within range."""
        self.assertTrue(self.enemy._is_within_range(0, 0, 1))
        self.assertFalse(self.enemy._is_within_range(10, 10, 5))

if __name__ == '__main__':
    unittest.main()

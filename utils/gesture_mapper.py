def gesture_mapper(finger_count=0):
  """
  Returns the name of the hand gesture based on the number of fingers.

  Args:
      finger_count (int): The number of fingers detected.

  Returns:
      str: The name of the corresponding hand gesture.
            Defaults to "Lizard" if the count is not recognized.
  """
  # Mapping of finger counts to gesture names
  finger_count_to_name = {
      0: "Rock",
      2: "Scissors",
      3: "Spock",
      5: "Paper",
  }

  # Return the gesture name or "Lizard" if the count is not in the mapping
  return finger_count_to_name.get(finger_count, "Lizard")
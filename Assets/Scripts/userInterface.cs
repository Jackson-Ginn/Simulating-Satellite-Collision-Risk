using UnityEngine;
using UnityEngine.UI;

public class userInterface : MonoBehaviour
{
    private Text timeText;

    private float initialTime;
    private float currentTime;
    private string timeString;
    private int totalMinutes;
    void Start()
    {
        // Get the Text component attached to this GameObject
        timeText = GetComponent<Text>();

        initialTime = Time.time;
        currentTime = 0;
    }
    void Update()
    {
        currentTime = Time.time - initialTime;

        int totalMinutes = Mathf.FloorToInt(currentTime / 60f);
        int days = totalMinutes / (24 * 60);
        int hours = (totalMinutes % (24 * 60)) / 60;
        int minutes = totalMinutes % 60;       

        timeString = string.Format("Simulation Time: {0}d {1}h {2}m", days, hours, minutes);
    
        timeText.text = timeString;
    }
}

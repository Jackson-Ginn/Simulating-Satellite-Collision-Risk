using UnityEngine;
using UnityEngine.UI;

public class userInterface : MonoBehaviour
{
    [SerializeField] private orbitCamera cameraController;

    private Text uiText;

    private float initialTime;

    void Start()
    {
        uiText = GetComponent<Text>();
        initialTime = Time.time;
    }

    void Update()
    {
        float currentTime = Time.time - initialTime;

        int totalMinutes = Mathf.FloorToInt(currentTime / 60f);
        int days = totalMinutes / (24 * 60);
        int hours = (totalMinutes % (24 * 60)) / 60;
        int minutes = totalMinutes % 60;

        string timeString = string.Format(
            "Simulation Time: {0}d {1}h {2}m",
            days, hours, minutes
        );

        string satelliteString = "";

        if (cameraController != null && cameraController.IsAttachedToSatellite)
        {
            satelliteString = "\nPOV: " + cameraController.CurrentSatelliteName;
        }

        uiText.text = timeString + satelliteString;
    }
}
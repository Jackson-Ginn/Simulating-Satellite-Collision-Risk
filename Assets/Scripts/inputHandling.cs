using UnityEngine;

public class inputHandling : MonoBehaviour
{
    [Header("User Input Settings for Simulation Control")]
    // Simulation pause and resume keys
    public KeyCode pause = KeyCode.Escape;
    public KeyCode resume = KeyCode.Space;

    // Simulation speed control keys
    public KeyCode speedOne = KeyCode.Alpha1;
    public KeyCode speedTwo = KeyCode.Alpha2;
    public KeyCode speedThree = KeyCode.Alpha3;

    // Remembering previous speed setting
    private float previousSpeedSetting;
    
    public float timeScale = 1.0f;

    // Update is called once per frame
    void Update()
    {
        if (Input.GetKeyDown(pause))
        {
            previousSpeedSetting = Time.timeScale;
            Time.timeScale = 0f; // Pause simulation
        }
        else if (Input.GetKeyDown(resume))
        {
            Time.timeScale = previousSpeedSetting; // Resume simulation at previous speed
        }
        else if (Input.GetKeyDown(speedOne))
        {
            Time.timeScale = 1f; // Set simulation speed to 1x
            timeScale = 1f;
        }
        else if (Input.GetKeyDown(speedTwo))
        {
            Time.timeScale = 5; // Set simulation speed to 5x 
            timeScale = 5f;
        }
        else if (Input.GetKeyDown(speedThree))
        {
            Time.timeScale = 60; // Set simulation speed to 60x
            timeScale = 60f;
        }
    }
}

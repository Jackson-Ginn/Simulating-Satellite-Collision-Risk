using UnityEngine;

public class CameraInputHandling : MonoBehaviour
{
    // Camera control keys
    public KeyCode panUp = KeyCode.W;
    public KeyCode panLeft = KeyCode.A;
    public KeyCode panDown = KeyCode.S;
    public KeyCode panRight = KeyCode.D;

    public KeyCode changeCam = KeyCode.C;
    public KeyCode resetCam = KeyCode.R;

    // Zoom control keys
    public KeyCode zoomIn = KeyCode.Q;
    public KeyCode zoomOut = KeyCode.E;

    // Camera movement speed
    private float cameraSpeed = 100.0f;

    // Camera position variables
    private Vector3 cameraPos;
    private Vector3 previousCameraPos;
    private Vector3 newCameraPos;
    private Vector3 initialCameraPos;
    private Vector3 cameraTopDown;
    private float cameraPosRadius;

    // Camera state variables
    private string cameraStatus = "Panning";
    private bool changeCamPressed = false;
    private bool resetCamPressed = false;
    private float currentTime;

    // Start is called once before the first execution of Update after the MonoBehaviour is created
    void Start()
    {
        cameraPos = transform.position;
        initialCameraPos = cameraPos;
        cameraPosRadius = cameraPos.magnitude;
        currentTime = Time.time;
        cameraTopDown = new Vector3(0, cameraPosRadius, 0);
    }

    // Update is called once per frame
    void Update()
    {
        // Calculate angular displacement
        float dt = Time.deltaTime/Time.timeScale;
        float angle = (float)(cameraSpeed * dt / cameraPosRadius);
       
        // Rotate camera position based on input
        if (Input.GetKey(changeCam))
        {
            // If camera is panning, switch to top down view
            if (cameraStatus == "Panning" && !changeCamPressed)
            {
                cameraStatus = "Top Down";
                previousCameraPos = cameraPos;
                cameraPos = cameraTopDown;
                changeCamPressed = true;
            }
            // If camera is in top down view, switch to panning
            else if (cameraStatus == "Top Down" && !changeCamPressed)
            {
                cameraPos = previousCameraPos;
                cameraStatus = "Panning";
                changeCamPressed = true;
            }
        }
        // Detect key release to reset debounce
        if (Input.GetKeyUp(changeCam) && changeCamPressed)
        {
            changeCamPressed = false;
        }
      
        // Reset camera position to initial if reset key pressed
        if (Input.GetKey(resetCam))
        {
            if (!resetCamPressed)
            {
                cameraPos = initialCameraPos;
                cameraStatus = "Panning";
                resetCamPressed = true;
                Debug.Log("Camera position reset");
            }
        }
        // Detect key release to reset debounce
        if (Input.GetKeyUp(resetCam) && resetCamPressed)
        {
            resetCamPressed = false;
        }
        
        // Camera panning control
        if (Input.GetKey(panUp))
        {
            newCameraPos = new Vector3(
                cameraPos.x * Mathf.Cos(-angle) - cameraPos.y * Mathf.Sin(-angle),
                cameraPos.x * Mathf.Sin(-angle) + cameraPos.y * Mathf.Cos(-angle),
                cameraPos.z
            );
            cameraPos = newCameraPos;
        }
        if (Input.GetKey(panDown))
        {
            newCameraPos = new Vector3(
                cameraPos.x * Mathf.Cos(angle) - cameraPos.y * Mathf.Sin(angle),
                cameraPos.x * Mathf.Sin(angle) + cameraPos.y * Mathf.Cos(angle),
                cameraPos.z
            );
            cameraPos = newCameraPos;
        }
        if (Input.GetKey(panLeft))
        {
            newCameraPos = new Vector3(
                cameraPos.x * Mathf.Cos(-angle) - cameraPos.z * Mathf.Sin(-angle),
                cameraPos.y,
                cameraPos.x * Mathf.Sin(-angle) + cameraPos.z * Mathf.Cos(-angle)
            );
            cameraPos = newCameraPos;
        }
        if (Input.GetKey(panRight))
        {
            newCameraPos = new Vector3(
                cameraPos.x * Mathf.Cos(angle) - cameraPos.z * Mathf.Sin(angle),
                cameraPos.y,
                cameraPos.x * Mathf.Sin(angle) + cameraPos.z * Mathf.Cos(angle)
            );
            cameraPos = newCameraPos;
        }

        // Camera zoom control
        cameraPos *= Input.mouseScrollDelta.y;

        // Don't let camera go further than 1000 units away
        if (cameraPos.magnitude > 1000.0f)
        {
            cameraPos = cameraPos.normalized * 1000.0f;
        }
        // Don't let camera get closer than 150 units
        if (cameraPos.magnitude < 150.0f)
        {
            cameraPos = cameraPos.normalized * 150.0f;
        }
        
        // Update camera position
        transform.position = cameraPos;

        // Point camera at origin
        transform.LookAt(Vector3.zero);


        // Log camera position radius every second
        if (Time.time > currentTime + 1.0f*Time.timeScale)
        {
            cameraPosRadius = transform.position.magnitude;

            //Debug.Log("Camera Position Radius: " + cameraPosRadius.ToString());

            currentTime = Time.time;
        }
    }
}

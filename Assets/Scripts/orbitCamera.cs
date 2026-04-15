using UnityEngine;

public class orbitCamera : MonoBehaviour
{
    [SerializeField] private float zoomSensitivity = 30f;
    [SerializeField] private float panSensitivity = 10f;
    [SerializeField] private float minOrbitRadius = 150f;
    [SerializeField] private float maxOrbitRadius = 1000f;
    [SerializeField] private float minPitch = -80f;
    [SerializeField] private float maxPitch = 80f;


    private float orbitRadius;
    private float mouseX;
    private float mouseY;
    private float pitch;

    private void Awake()
    {
        orbitRadius = transform.position.magnitude;
    }

    private void Update()
    {
        // Mouse orbit control
        if (Input.GetMouseButton(0))
        {
            // Look at origin
            transform.LookAt(Vector3.zero);
            // Mouse axis delta to orbit angles
            mouseX = Input.GetAxis("Mouse X") * panSensitivity;
            mouseY = Input.GetAxis("Mouse Y") * panSensitivity;    
            pitch = Mathf.Clamp(pitch, minPitch, maxPitch);
            transform.eulerAngles += new Vector3(-mouseY, mouseX, 0);
        }
        // Touch orbit control
        //if (Input.)

        // Mouse zoom control
        orbitRadius -= Input.mouseScrollDelta.y * zoomSensitivity;
        orbitRadius = Mathf.Clamp(orbitRadius, minOrbitRadius, maxOrbitRadius);

        transform.position = Vector3.zero - transform.forward * orbitRadius;
    }
}

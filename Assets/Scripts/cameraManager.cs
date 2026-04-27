using UnityEngine;
using System.Collections.Generic;

public class orbitCamera : MonoBehaviour
{
    [SerializeField] private satelliteManagerV2 satManager;

    [Header("Orbit Camera Settings")]
    [SerializeField] private Camera targetCamera;
    [SerializeField] private float zoomSensitivity = 30f;
    [SerializeField] private float panSensitivity = 10f;
    [SerializeField] private float minOrbitRadius = 150f;
    [SerializeField] private float maxOrbitRadius = 1000f;
    [SerializeField] private float minPitch = -80f;
    [SerializeField] private float maxPitch = 80f;
    private Vector3 orbitCameraPosition;
    private float orbitRadius;
    private float mouseX;
    private float mouseY;
    private float pitch;
    private bool orbit = true;

    [Header("Camera follow settings")]
    private bool keepUpdatingWhileAttached = true;
    private List<typeSatellite> sats;
    private int satIndex = 0;
    private int satCount;
    private bool satListFetched = false;
    private bool justCycled = false;
    Quaternion pointCamera;

    public bool IsAttachedToSatellite => !orbit;

    public string CurrentSatelliteName
    {
        get
        {
            if (!satListFetched || sats == null || sats.Count == 0)
                return "";

            return sats[satIndex].name;
        }
    }

    
    private void Awake()
    {
        orbitRadius = targetCamera.transform.position.magnitude;
    }


// Stored angles for the camera
float headingAngle, pitchAngle;
Quaternion initalCameraRotation;
    private void LateUpdate()
    {
        // Orbit Camera Control
        if (orbit == true)
            {
            // Mouse orbit control
            if (Input.GetMouseButton(0))
            {
                // Look at origin
                targetCamera.transform.LookAt(Vector3.zero);
                // Mouse axis delta to orbit angles
                mouseX = Input.GetAxis("Mouse X") * panSensitivity;
                mouseY = Input.GetAxis("Mouse Y") * panSensitivity;    


                pitch = Mathf.Clamp(pitch, minPitch, maxPitch);
                targetCamera.transform.eulerAngles += new Vector3(-mouseY, mouseX, 0);
            }
            // Mouse zoom control
            orbitRadius -= Input.mouseScrollDelta.y * zoomSensitivity;
            orbitRadius = Mathf.Clamp(orbitRadius, minOrbitRadius, maxOrbitRadius);

            targetCamera.transform.position = Vector3.zero - targetCamera.transform.forward * orbitRadius;

            // Change to satellite camera
            if (Input.GetKeyDown(KeyCode.C))
            {
                orbit = false;
                orbitCameraPosition = targetCamera.transform.position;
            }
        }
        // Satellite Camera Control
        else
        {
            if (!satListFetched)
            {
                sats = satManager.Satellites;
                satCount = sats.Count;
                satListFetched = true;
            }

            cycleIndex(satCount);

            typeSatellite sat = sats[satIndex];

            Vector3 satPosition = sat.transform.position;

            pointCamera = Quaternion.LookRotation(sat.velocity, Vector3.Normalize(satPosition));
            initalCameraRotation = pointCamera;

            // Set inital camera point to velocity vector direction
            if (justCycled)
            {
                justCycled = false;
                pitchAngle = 0;
                headingAngle = 0;
            }
            // Allow user to pan camera around satellite
            else
            {   
                if (Input.GetMouseButton(0))
                {
                    float mouseX = Input.GetAxis("Mouse X");
                    float mouseY = Input.GetAxis("Mouse Y");

                    Vector3 yawAxis = Vector3.Normalize(satPosition);
                    Vector3 pitchAxis = Vector3.Normalize(Vector3.Cross(sat.velocity, satPosition));

                    //Quaternion align = Quaternion.FromToRotation(transform.up, rotationAxis);
                    //targetCamera.transform.rotation = align * transform.rotation;   

                    headingAngle += mouseX * panSensitivity;
                     pitchAngle += mouseY * panSensitivity;

                    pointCamera = Quaternion.AngleAxis(headingAngle, yawAxis) * Quaternion.AngleAxis(pitchAngle, pitchAxis) * initalCameraRotation;
                    
                }
            }
            targetCamera.transform.SetPositionAndRotation(satPosition, pointCamera);

            // Change to orbit camera
            if (Input.GetKeyDown(KeyCode.C))
            {
                orbit = true;
                targetCamera.transform.position = orbitCameraPosition;
                targetCamera.transform.LookAt(Vector3.zero);
            }
        }
    }
    private void cycleIndex(int count)
    {
        if (Input.GetKeyDown(KeyCode.UpArrow))
        {
            satIndex = (satIndex + 1) % count;
            justCycled = true;
        }

        if (Input.GetKeyDown(KeyCode.DownArrow))
        {
            satIndex = (satIndex - 1 + count) % count;
            justCycled = true;
        }
    }   
}
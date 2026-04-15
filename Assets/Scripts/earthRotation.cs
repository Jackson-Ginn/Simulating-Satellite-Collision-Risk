using UnityEngine;

public class earth_rotation : MonoBehaviour
{
    // Earth rotation speed 
    private float rotationSpeed = -360/86164.091f;

    // Update is called once per frame
    void FixedUpdate()
    {
        transform.Rotate(Vector3.up, rotationSpeed * Time.fixedDeltaTime);
    }
}
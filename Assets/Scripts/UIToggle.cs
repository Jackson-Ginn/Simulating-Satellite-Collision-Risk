using UnityEngine;

public class UIToggle : MonoBehaviour
{
    public GameObject uiRoot;

    void Update()
    {
        if (Input.GetKeyDown(KeyCode.H))
        {
            uiRoot.SetActive(!uiRoot.activeSelf);
        }
    }
}

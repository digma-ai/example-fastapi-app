using System.Diagnostics;
using Microsoft.AspNetCore.Mvc;

namespace dotnet_api_example.Controllers;

[ApiController]
[Route("[controller]")]
public class FullController : ControllerBase
{
    private static readonly ActivitySource Activity = new ActivitySource("FullController");

    public FullController()
    {
    }

    [HttpGet(Name = "full")]
    public string Get()
    {
        using (var activity = Activity.StartActivity("Full Route", ActivityKind.Producer)) {
            return "This route is full...";
        }
    }
}

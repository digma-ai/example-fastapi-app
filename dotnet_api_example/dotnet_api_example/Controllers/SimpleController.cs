using System.Diagnostics;
using Microsoft.AspNetCore.Mvc;

namespace dotnet_api_example.Controllers;

[ApiController]
[Route("[controller]")]
public class SimpleController : ControllerBase
{
    private static readonly ActivitySource Activity = new("SimpleController");

    public SimpleController()
    {
    }

    [HttpGet(Name = "simple")]
    public string Get()
    {
        using (var activity = Activity.StartActivity("Simple Route", ActivityKind.Producer)) {
            throw new Exception("Blah");
        }
    }
}

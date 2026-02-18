using FamilyFinance.Application.Interfaces;
using FamilyFinance.Domain.Repositories;
using FamilyFinance.Infrastructure.Repositories;
using FamilyFinance.Infrastructure.Services;

var builder = WebApplication.CreateBuilder(args);

// Add services to the container.
builder.Services.AddSingleton<ITransactionRepository, FakeTransactionRepository>();

builder.Services.AddHttpClient<IAiService, AiServiceClient>(client =>
    client.BaseAddress = new Uri(builder.Configuration["AiService:BaseUrl"] ?? "http://localhost:8000"));

builder.Services.AddControllers();
builder.Services.AddEndpointsApiExplorer();
builder.Services.AddSwaggerGen();

var app = builder.Build();

// Configure the HTTP request pipeline.
if (app.Environment.IsDevelopment())
{
    app.UseSwagger();
    app.UseSwaggerUI();
}

app.UseHttpsRedirection();

app.UseAuthorization();

app.MapControllers();

app.Run();

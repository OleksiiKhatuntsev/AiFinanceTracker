using FamilyFinance.Application.Dto;
using FamilyFinance.Application.Mappings;
using FamilyFinance.Domain.Repositories;

using Microsoft.AspNetCore.Mvc;

namespace FamilyFinance.Api.Controllers;

[ApiController]
[Route("[controller]")]
public class TransactionsController(ITransactionRepository transactionRepository) : ControllerBase
{
    [HttpPost("Random")]
    public ActionResult<IEnumerable<TransactionDto>> GetRandom()
    {
        var transactions = transactionRepository
            .GetAll()
            .Select(t => t.ToDto())
            .ToList();

        return Ok(transactions);
    }
}

using FamilyFinance.Domain.Entities;

namespace FamilyFinance.Domain.Repositories;

public interface ITransactionRepository
{
    IReadOnlyList<Transaction> GetAll();
}

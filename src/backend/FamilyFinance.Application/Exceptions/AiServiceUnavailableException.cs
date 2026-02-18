namespace FamilyFinance.Application.Exceptions;

public class AiServiceUnavailableException(Exception? innerException = null)
    : Exception("The AI service is currently unavailable. Please try again later.", innerException);

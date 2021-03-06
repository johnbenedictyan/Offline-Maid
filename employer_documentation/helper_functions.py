from onlinemaid.constants import FullNationsChoices

from .constants import (EmployerTypeOfApplicantChoices,
                        ResidentialStatusFullChoices)


def is_local(rs) -> bool:
    return (
        rs == ResidentialStatusFullChoices.SC
        or rs == ResidentialStatusFullChoices.PR
    )


def is_foreigner(rs) -> bool:
    return not is_local(rs)


def is_applicant_sponsor(type_of_applicant) -> bool:
    return type_of_applicant == EmployerTypeOfApplicantChoices.SPONSOR


def is_applicant_joint_applicant(type_of_applicant) -> bool:
    return type_of_applicant == EmployerTypeOfApplicantChoices.JOINT_APPLICANT


def is_applicant_spouse(type_of_applicant) -> bool:
    return type_of_applicant == EmployerTypeOfApplicantChoices.SPOUSE


def nationality_residential_status_match(n, rs) -> bool:
    if n == FullNationsChoices.SINGAPORE:
        return rs == ResidentialStatusFullChoices.SC
    elif rs == ResidentialStatusFullChoices.SC:
        return n == FullNationsChoices.SINGAPORE
    else:
        return True

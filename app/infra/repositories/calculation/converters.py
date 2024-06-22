from app.domain.entities.packages import PackageCalculationLog


def convert_log_entity_to_document(log: PackageCalculationLog) -> dict:
    return {
        'oid': log.oid,
        'type_id': log.type_id,
        'value': log.value,
        'date': log.date,
    }

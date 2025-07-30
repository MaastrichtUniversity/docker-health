package com.medblocks.openfhir.db.repository.mongodb;

import com.medblocks.openfhir.db.entity.FhirConnectContextEntity;
import com.medblocks.openfhir.db.repository.FhirConnectContextRepository;
import lombok.NonNull;
import org.springframework.data.mongodb.repository.MongoRepository;
import org.springframework.data.mongodb.repository.Query;

public interface FhirConnectContextMongoRepository extends FhirConnectContextRepository, MongoRepository<FhirConnectContextEntity, String> {

    @Query("{'fhirConnectContext.context.template.id': ?0}")
    FhirConnectContextEntity findByTemplateId(final String templateId);

    @Query("{'id': ?0}")
    FhirConnectContextEntity byId(@NonNull final String id);
}

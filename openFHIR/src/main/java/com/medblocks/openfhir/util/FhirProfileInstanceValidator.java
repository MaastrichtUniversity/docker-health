package com.medblocks.openfhir.util;

import ca.uhn.fhir.context.FhirContext;
import ca.uhn.fhir.context.support.DefaultProfileValidationSupport;
import ca.uhn.fhir.parser.IParser;
import ca.uhn.fhir.validation.FhirValidator;
import ca.uhn.fhir.validation.ValidationResult;
import lombok.extern.slf4j.Slf4j;
import org.hl7.fhir.common.hapi.validation.support.CommonCodeSystemsTerminologyService;
import org.hl7.fhir.common.hapi.validation.support.InMemoryTerminologyServerValidationSupport;
import org.hl7.fhir.common.hapi.validation.support.PrePopulatedValidationSupport;
import org.hl7.fhir.common.hapi.validation.support.ValidationSupportChain;
import org.hl7.fhir.common.hapi.validation.validator.FhirInstanceValidator;
import org.hl7.fhir.r4.model.StructureDefinition;
import org.hl7.fhir.r4.model.ValueSet;
import org.springframework.core.io.support.PathMatchingResourcePatternResolver;
import org.springframework.core.io.support.ResourcePatternResolver;
import org.springframework.http.HttpStatus;
import org.springframework.web.server.ResponseStatusException;

import java.io.IOException;


@Slf4j
public class FhirProfileInstanceValidator {
    private final FhirContext fhirContext = FhirContext.forR4();

    public FhirProfileInstanceValidator() {
    }


    public ValidationResult instanceValidator(String incomingFhirResource) {
//        final Resource fhirResource = parseIncomingFhirResource(incomingFhirResource);

        // Create a chain that will hold our modules and caches the values they supply
        ValidationSupportChain supportChain = new ValidationSupportChain();

        // DefaultProfileValidationSupport supplies base FHIR definitions. This is generally required
        // even if you are using custom profiles, since those profiles will derive from the base
        // definitions.
        DefaultProfileValidationSupport defaultSupport = new DefaultProfileValidationSupport(fhirContext);
        defaultSupport.fetchAllStructureDefinitions();
        defaultSupport.fetchCodeSystem("");
        supportChain.addValidationSupport(defaultSupport);

        // This module supplies several code systems that are commonly used in validation
        supportChain.addValidationSupport(new CommonCodeSystemsTerminologyService(fhirContext));

        // This module implements terminology services for in-memory code validation
        supportChain.addValidationSupport(new InMemoryTerminologyServerValidationSupport(fhirContext));


        // Create a PrePopulatedValidationSupport which can be used to load custom definitions.
        // In this example we're loading two things, but in a real scenario we might
        // load many StructureDefinitions, ValueSets, CodeSystems, etc.
        PrePopulatedValidationSupport prePopulatedSupport = new PrePopulatedValidationSupport(fhirContext);
        IParser parser = fhirContext.newXmlParser();

        try {
            ResourcePatternResolver resourcePatternResolver = new PathMatchingResourcePatternResolver();
            for (org.springframework.core.io.Resource profileResource : resourcePatternResolver.getResources("classpath:/profiles/*")) {
                StructureDefinition profile = parser.parseResource(StructureDefinition.class, profileResource.getInputStream());
                prePopulatedSupport.addStructureDefinition(profile);
            }
            for (org.springframework.core.io.Resource profileResource : resourcePatternResolver.getResources("classpath:/valueset/*")) {
                ValueSet valueset = parser.parseResource(ValueSet.class, profileResource.getInputStream());
                prePopulatedSupport.addValueSet(valueset);
            }
        } catch (IOException e) {
            throw new ResponseStatusException(HttpStatus.INTERNAL_SERVER_ERROR, "An I/O exception occurred while loading custom profiles");
        }
        defaultSupport.fetchCodeSystem("");
        prePopulatedSupport.fetchAllStructureDefinitions();
        prePopulatedSupport.fetchAllConformanceResources();
        prePopulatedSupport.fetchAllSearchParameters();
        prePopulatedSupport.fetchAllNonBaseStructureDefinitions();

        supportChain.fetchAllStructureDefinitions();
        supportChain.fetchAllConformanceResources();
        supportChain.fetchAllSearchParameters();
        supportChain.fetchAllNonBaseStructureDefinitions();

        // Add the custom definitions to the chain
        supportChain.addValidationSupport(prePopulatedSupport);

        // Create a validator using the FhirInstanceValidator module. We can use this
        // validator to perform validation
        FhirInstanceValidator validatorModule = new FhirInstanceValidator(supportChain);
        validatorModule.setAnyExtensionsAllowed(true);
        FhirValidator validator = fhirContext.newValidator().registerValidatorModule(validatorModule);

        return validator.validateWithResult(incomingFhirResource);
    }
}